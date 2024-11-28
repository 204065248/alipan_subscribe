"""导出分享中所有文件信息"""
from aligo import Aligo, EMailConfig, set_config_folder
import alipan_email
from datetime import datetime
from config import Config


def tree_folder(ali, folder_file_list, parent_file_id='root', share_token=None, drive_id=None):
    if share_token:
        file_list = ali.get_share_file_list(
            share_token, parent_file_id=parent_file_id)
    else:
        file_list = ali.get_file_list(
            parent_file_id=parent_file_id, drive_id=drive_id)
    for file in file_list:
        folder_file_list.append(file)
        if file.type == 'folder':
            tree_folder(ali, folder_file_list,
                        file.file_id, share_token, drive_id)


def compare_file_lists(ali, share_files, share_token, parent_file_id, my_files, to_parent_file_id, drive_id):
    differences = []
    my_file_dict = {f.name: f for f in my_files}
    exclude_file_ids = []
    for share_file in share_files:
        my_file = my_file_dict.get(share_file.name)
        if not my_file:
            if share_file.parent_file_id == parent_file_id:
                my_parent = ali.get_file(to_parent_file_id, drive_id)
                exclude_file_ids.append(share_file.file_id)
            else:
                if share_file.parent_file_id in exclude_file_ids:
                    continue
                share_parent = ali.get_share_file(
                    share_file.parent_file_id, share_token)
                my_parent = my_file_dict.get(share_parent.name)
                if share_file.type == 'folder' and not my_parent:
                    exclude_file_ids.append(share_file.file_id)
            differences.append(
                {'item': share_file, 'parent': my_parent, 'desc': ''})
    return differences


def diff_save_to_drive(ali, differences, share_token, resource_drive_id, auto_rename=True):
    for diff in differences:
        item = diff['item']
        parent = diff['parent']
        if parent:
            res = ali.batch_share_file_saveto_drive(
                [item.file_id], share_token, to_parent_file_id=parent.file_id, to_drive_id=resource_drive_id, auto_rename=auto_rename)
            datetime_obj = datetime.fromisoformat(
                item.updated_at.replace("Z", "+00:00"))
            formatted_time = datetime_obj.strftime(
                "%Y年%m月%d日 %H:%M:%S")  # 自定义输出格式
            if res[0].status == 201 or res[0].status == 202:
                desc = f'最后更新于: {formatted_time}，已保存到 {parent.name} 文件夹'
            else:
                desc = f'最后更新于: {formatted_time}，保存失败, 状态码 {res[0].status}'
            diff['desc'] = desc
        else:
            diff['desc'] = f'文件 {item.name} 未找到父文件夹'


def main():
    # 修改这里
    for user in config.ali_user_configs:
        email_config = EMailConfig(email=user.email_address, host=alipan_email.smtp_server,
                                   port=alipan_email.smtp_port, user=alipan_email.smtp_user, password=alipan_email.smtp_password)
        ali = Aligo(name=user.config_name, email=email_config)

        for task in user.task_configs:
            if task.share_pwd:
                share_token = ali.get_share_token(
                    task.share_id, task.share_pwd)
            else:
                share_token = ali.get_share_token(task.share_id)
            share_folder_file_list = []
            tree_folder(ali, share_folder_file_list,
                        task.parent_file_id, share_token)

            if task.is_resource_disk:
                v2_user = ali.v2_user_get()
                resource_drive_id = v2_user.resource_drive_id
            else:
                resource_drive_id = None

            myfolder_file_list = []
            tree_folder(ali=ali, folder_file_list=myfolder_file_list,
                        parent_file_id=task.to_parent_file_id, drive_id=resource_drive_id)

            differences = compare_file_lists(
                ali, share_folder_file_list, share_token, task.parent_file_id, myfolder_file_list, task.to_parent_file_id, resource_drive_id)
            if not differences:
                print('没有发现新文件')
                continue
            diff_save_to_drive(
                ali, differences, share_token, resource_drive_id)
            alipan_email.send_html(
                user.email_address, user.nickname, task.task_name, differences)


if __name__ == '__main__':
    set_config_folder('./aligo')
    config = Config()
    config.init_config()
    alipan_email.smtp_server = config.email.smtp_server
    alipan_email.smtp_port = config.email.smtp_port
    alipan_email.smtp_user = config.email.smtp_user
    alipan_email.smtp_password = config.email.smtp_password
    main()
