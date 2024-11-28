import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = 'smtp.example.com'  # SMTP 服务器
smtp_port = 25  # SMTP 端口
smtp_user = 'example@163.com'  # 发送方邮箱
smtp_password = ''  # 发送方邮箱密码

def send_html(to_email, to_name, subject, updates):
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    # 创建邮件正文
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
                max-width: 600px;
                margin: auto;
            }}
            h1 {{
                color: #333;
            }}
            p {{
                color: #555;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #007BFF;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>更新通知</h1>
            <p>亲爱的 {to_name}，</p>
            <p>{subject}发生了更新，更新内容如下：</p>
            <table>
                <tr>
                    <th>更新项</th>
                    <th>描述</th>
                </tr>
    """
    
    # 将更新内容添加到表格中
    for diff in updates:
        item = diff['item']
        parent = diff['parent']
        desc = diff['desc']
        if parent:
            html_content += f"""
                <tr>
                    <td>{item.name}</td>
                    <td>{desc}</td>
                </tr>
            """
        else:
            html_content += f"""
                <tr>
                    <td>{item.name}</td>
                    <td>父级目录不存在，请反馈给作者。</td>
                </tr>
            """
    
    html_content += """
            </table>
            <div class="footer">
                <p>若链接文件内容过多，则可能无法立即生效，请耐心等待，感谢您的关注！</p>
            </div>
        </div>
    </body>
    </html>
    """


    # 将HTML正文添加到邮件中
    msg.attach(MIMEText(html_content, 'html'))

    # 发送邮件
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 使用TLS
            server.login(smtp_user, smtp_password)  # 登录
            server.sendmail(smtp_user, to_email, msg.as_string())  # 发送邮件
        print("邮件发送成功!")
    except Exception as e:
        print(f"邮件发送失败: {e}")


if __name__ == '__main__':
    send_html('33762626@qq.com', '收件人昵称', '邮件标题', {'更新项1': '描述1', '更新项2': '描述2'})