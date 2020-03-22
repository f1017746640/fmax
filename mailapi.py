#!/usr/bin/env python
# encoding: utf-8
"""
   > FileName: mailapi.py
   > Author: FZH
   > Mail: fengzhihai@ilarge.cn
   > CreatedTime: 2020-03-22 13:20
"""
import os
import requests

url = "http://127.0.0.1:5000/fmax"


def mail_send():
    data = {'mail_to': 'fengzhihai@ilarge.cn',
            'mail_title': 'TEST_TITLE',
            'mail_body': '接口更新完毕'}
    files = []
    response = requests.request("POST",
                                url,
                                data=data,
                                files=files)
    return response.text.encode('utf8')


def mail_send_append():
    data = {'mail_to': 'fengzhihai@ilarge.cn',
            'mail_title': 'TEST_TITLE',
            'mail_body': '接口更新完毕'}

    des_file = os.path.join(os.path.dirname(__file__),
                            'fmax.xlsx')
    files = {'file': open(des_file, 'rb')}
    headers = {
      'Content-Type': 'multipart/form-data'
    }
    response = requests.request("POST",
                                url,
                                data=data,
                                files=files)
    return response.text.encode('utf8')


if __name__ == '__main__':
    mail_send_append()
