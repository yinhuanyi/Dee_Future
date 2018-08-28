#!/usr/bin/env python  
#-*- coding:utf-8 _*-  


import random


from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from Future_Edu.settings import EMAIL_FROM
import logging
logger = logging.getLogger('django_debug_error')


def generate_ramdom_str(random_length=8):
    string = ""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = len(chars) - 1
    for _ in range(random_length):
        string += chars[random.randint(0, length)]
    return string


def send_register_email(email, send_type="register"):

    email_record = EmailVerifyRecord()
    code = generate_ramdom_str(4) if send_type == "update_email" else generate_ramdom_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "Dee Future教学管理系统在线注册链接"
        email_body = "请点击下边的连接，激活您的账号: http://192.168.199.209:12345/users/active/{}".format(code)
        # email_body = "请点击下边的连接，激活您的账号: http://deefuture.yhyblog.cn/active/{}".format(code) # 部署
        send_status = send_mail(subject=email_title, message=email_body, from_email=EMAIL_FROM, recipient_list=[email],)
        if send_status:
            logger.debug(send_status)
            return True
        else:
            logger.error(send_status)
            return False


    elif send_type == 'forget':
        email_title = "Dee Future教学管理系统密码重置链接"
        email_body = "请点击下边的连接，重置您的密码: http://192.168.199.209:12345/users/reset/{}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            logger.debug(send_status)
            return True
        else:
            logger.error(send_status)
            return False


    elif send_type == "update_email":
        email_title = "Dee Future教学管理系统修改邮箱"
        email_body = "您的邮箱验证码是：{}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            logger.debug(send_status)
            return True
        else:
            logger.error(send_status)
            return False



















