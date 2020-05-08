#!/usr/bin/env python
# encoding: utf-8
"""
   > FileName: app.py
   > Author: FZH
   > Mail: fengzhihai@xxx.cn
   > CreatedTime: 2020-03-22 11:34
"""
import os
import json
from flask import request
from flask import Flask
from werkzeug.utils import secure_filename
from mailer import mailer

app = Flask(__name__)


# 1.邮件发送的接口
@app.route('/fmax', methods=['POST'])
def fmax():
    if request.method == "POST":
        mail_host = request.form.get("mail_host")
        mail_password = request.form.get("mail_password")
        mail_to = request.form.get("mail_to")
        mail_title = request.form.get("mail_title")
        mail_body = request.form.get("mail_body")
        mail_append = request.files.get("file")
        if mail_to is None or mail_title is None or mail_body is None:
            msg = "mail_to,mail_title,mail_body is necessary," \
                  "mail_append,mail_host,mail_password is optional."
            print(msg)
            roll_msg = {"message": msg}
            return json.dumps(roll_msg), 400
        if mail_append:
            pathname = './' + secure_filename(mail_append.filename)
            mail_append.save(pathname)
        else:
            pathname = None
        ret = mailer(mail_to=mail_to,
                     mail_title=mail_title,
                     mail_body=mail_body,
                     mail_append=pathname,
                     mail_host=mail_host,
                     mail_password=mail_password)
        if ret:
            msg = 'mail send success.'
            print(msg)
            roll_msg = {"message": msg}
            return json.dumps(roll_msg), 200
        else:
            msg = 'mail send fail.'
            print(msg)
            roll_msg = {"message": msg}
            return json.dumps(roll_msg), 500
    else:
        msg = 'Method Not Allowed.'
        print(msg)
        roll_msg = {"message": msg}
        return json.dumps(roll_msg), 400
