import yaml

class EmailConfig:
    def __init__(self):
        self.smtp_server = ''
        self.smtp_port = 0
        self.smtp_user = ''
        self.smtp_password = ''

class TaskConfig:
    def __init__(self):
        self.task_name = ''
        self.parent_file_id = ''
        self.to_parent_file_id = ''
        self.share_id = ''
        self.share_pwd= ''
        self.is_resource_disk = False

class AliUserConfig:
    def __init__(self):
        self.config_name = ''
        self.email_address = ''
        self.nickname = ''
        self.task_configs = []

class Config:
    def __init__(self):
        self.email = EmailConfig()
        self.ali_user_configs = []
        self.port = 1234

    def init_config(self):
        # 读取config.yml
        with open('config.yml', 'r', encoding='utf-8') as f:
            config_content = yaml.load(f, Loader=yaml.FullLoader)
        # 读取配置
        self.port = config_content['port']
        self.email.smtp_server = config_content['email']['smtp_server']
        self.email.smtp_port = config_content['email']['smtp_port']
        self.email.smtp_user = config_content['email']['smtp_user']
        self.email.smtp_password = config_content['email']['smtp_password']
        for user_config in config_content['ali_user_configs']:
            ali_user_config = AliUserConfig()
            ali_user_config.config_name = user_config['config_name']
            ali_user_config.email_address = user_config['email_address']
            ali_user_config.nickname = user_config['nickname']
            for task_config in user_config['task_configs']:
                task_config_obj = TaskConfig()
                task_config_obj.task_name = task_config['task_name']
                task_config_obj.parent_file_id = task_config['parent_file_id']
                task_config_obj.to_parent_file_id = task_config['to_parent_file_id']
                task_config_obj.share_id = task_config['share_id']
                task_config_obj.share_pwd = task_config['share_pwd']
                task_config_obj.is_resource_disk = task_config['is_resource_disk']
                ali_user_config.task_configs.append(task_config_obj)
            self.ali_user_configs.append(ali_user_config)
