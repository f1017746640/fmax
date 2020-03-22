#!/usr/bin/env python
# encoding: utf-8
"""
   > FileName: mailer
   > Author: FZH
   > Mail: fengzhihai@ilarge.cn
   > CreatedTime: 2020-03-22 11:58
"""
import os
import sys
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

config = configparser.ConfigParser()
config_file = "config.ini"
config.read(config_file)
sec = config["mail"]
MAIL_HOST = sec["MAIL_HOST"]
MAIL_PORT = sec["MAIL_PORT"]
MAIL_HOST_USER = sec["MAIL_HOST_USER"]
MAIL_HOST_PASSWORD = sec["MAIL_HOST_PASSWORD"]
MAIL_USER_TLS = sec["MAIL_USER_TLS"]
MAIL_FROM = sec["MAIL_FROM"]


def mailer(mail_to,
           mail_title,
           mail_body,
           mail_append=None,
           mail_host=None,
           mail_password=None):
    ret = True
    try:
        msg = MIMEMultipart()
        mail_from = mail_host or MAIL_FROM
        mail_host_user = mail_host or MAIL_HOST_USER
        mail_host_password = mail_password or MAIL_HOST_PASSWORD
        msg['From'] = mail_from
        msg['To'] = mail_to
        msg['Subject'] = mail_title

        # 添加内容信息
        text = MIMEText(mail_body)
        msg.attach(text)

        # 如果有附件，添加附近信息
        if mail_append:
                part = MIMEApplication(open(mail_append, 'rb').read())
                part.add_header('Content-Disposition', 'attachment',
                                filename=('gbk', '', mail_append.split('/')[-1]))
                msg.attach(part)

        server = smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT)
        server.login(mail_host_user, mail_host_password)
        server.sendmail(mail_from,
                        mail_to.split(','),
                        msg.as_string())
        server.quit()
    except Exception as e:
        ret = False
        print(e)
    finally:
        if mail_append:
            os.remove(mail_append)
    return ret


if __name__ == '__main__':
    if len(sys.argv[1:]) == 3:
        res = mailer(sys.argv[1],
                     sys.argv[2],
                     sys.argv[3])
    elif len(sys.argv[1:]) == 4:
        res = mailer(sys.argv[1],
                     sys.argv[2],
                     sys.argv[3],
                     sys.argv[4])
    else:
        res = False
    if res:
        print('mail send success')
    else:
        print('mail send fail')
