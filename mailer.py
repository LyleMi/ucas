#!/usr/bin/env python
# -*- coding: utf-8 -*-


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header


def sendemail(user, pwd, smtpServer, receiver):
    username = "同学"
    title = "选课成功通知"
    content = "选课已完成，请登录课程网站确认"
    receivers = [receiver]
    server = smtplib.SMTP_SSL(smtpServer, port=465)
    message = MIMEMultipart()
    message['From'] = Header('UCAS 选课插件', 'utf-8')
    message['To'] = Header(username, 'utf-8')
    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    text = MIMEText(content, 'html', 'utf-8')
    message.attach(text)

    try:
        server.login(user, pwd)
        server.sendmail(user, receivers, message.as_string())
        server.close()
        return True
    except smtplib.SMTPRecipientsRefused as e:
        print('Recipient refused')
    except smtplib.SMTPAuthenticationError as e:
        print('Auth error')
    except smtplib.SMTPSenderRefused as e:
        print('Sender refused')
    except smtplib.SMTPException as e:
        print(repr(e))
        return False
