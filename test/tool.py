import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
#发邮箱
def send_email(to_email, subject, content):
    # 邮箱配置
    smtp_server = "smtp.qq.com"  # QQ邮箱
    smtp_port = 465  # SSL端口
    from_email = ""  # 发件人邮箱
    password = ""  # 邮箱授权码，不是登录密码
    # 创建邮件对象
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = Header(subject, 'utf-8')
    # 添加邮件正文
    message.attach(MIMEText(content, 'plain', 'utf-8'))
    try:
        # 创建SMTP连接
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_email, password)
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        print("邮件发送成功！")
        return True
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return False