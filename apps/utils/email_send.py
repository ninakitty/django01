# coding:utf-8

__author__ = 'nina'
__date__ = '2018/1/4 16:28'
import random
from django.core.mail import send_mail
from django01.settings import EMAIL_FROM

from users.models import EmailVerifyRecord




def send_register_email(email, send_type='register'):
    # 生成及保存邮箱验证码
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件相关
    email_title = ''
    email_body = ""

    if send_type == 'register':
        email_title = '邮箱注册链接'
        email_body = "请点击下面链接激活帐号：http://127.0.0.1:8000/activate/{0}".format(code)
        email_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if email_status:
            pass


def random_str(randomlength=8):
    str1 = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    length = len(chars) - 1
    for i in range(randomlength):
        str1 += chars[random.randint(0, length)]
    return str1
