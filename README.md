# 阿里云分享链接订阅

## 介绍

阿里云分享链接订阅，追剧追番不再麻烦，搭配青龙面板使用，轻松实现自动化。

如果喜欢本项目，请给个star鼓励一下，谢谢！

## 配置文件

### 示例

```yaml
email:
  smtp_server: smtp.163.com
  smtp_port: 25
  smtp_user: xxxxxxxxxxxx@163.com
  smtp_password: xxxxxxxxxxx
ali_user_configs:
  - config_name: xxxxxxxxxx
    email_address: xxxxxxx@qq.com
    nickname: xxxxxxx
    task_configs:
      - task_name: xxxxxxxxx分享链接监听
        parent_file_id: xxxxxxxxxxxxxxxxxxxxxxxxx
        to_parent_file_id: xxxxxxxxxxxxxxxxxxxxxxxxx
        is_resource_disk: true
        share_id: xxxxxxxxxxx
        share_pwd: ''
      - task_name: xxxxxxxxxx分享链接监听
        parent_file_id: xxxxxxxxxxxxxxxxxxxxxxxxx
        to_parent_file_id: xxxxxxxxxxxxxxxxxxxxxxxxx
        is_resource_disk: true
        share_id: xxxxxxxxxxx
        share_pwd: ''
```

### 配置项说明

- `email`：用于发送邮件的配置项，包括：
  - `smtp_server`：SMTP服务器地址
  - `smtp_port`：SMTP服务器端口
  - `smtp_user`：SMTP用户名
  - `smtp_password`：SMTP密码
- `ali_user_configs`：阿里云用户配置项，包括：
  - `config_name`：用户配置名称，用于区分不同的阿里云账号
  - `email_address`：用户邮箱地址，用于接收订阅更新邮件，以及登录二维码邮件
  - `nickname`：用户昵称
  - `task_configs`：用户任务配置项，包括：
    - `task_name`：任务名称
    - `parent_file_id`：分享链接的阿里云目录ID，怎么获得ID详情百度
    - `to_parent_file_id`：要保存到你的阿里云的目录ID，怎么获得ID详情百度
    - `is_resource_disk`：要保存的目录是否为资源盘
    - `share_id`：分享链接ID，https://www.alipan.com/s/gA48oXbGQDc，其中gA48oXbGQDc就是分享链接ID
    - `share_pwd`：分享链接密码（可选）

# 声明

此项目仅供学习交流，若有不妥之处，侵联必删。