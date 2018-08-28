# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default=u'')
    birthday = models.DateField(verbose_name='生日', blank=True, null=True)
    gender = models.CharField(
        choices=(('male', '男'), ('female', '女')),
        default='male',
        max_length=50,
    )
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, default='')
    # upload to media directory
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)


    class Meta:
        # 用来描述这张表
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # todo: 获取用户未读消息的数量， 使得user可以调用这个函数获得未读消息的记录对象集合
    def get_unread_nums(self):
        from operation.models import UserMessage  # 避免发生循环导入
        return UserMessage.objects.filter(has_read=False, user=self.id).count()


# todo: need to optimize
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码"),("update_email", "修改邮箱") ), max_length=50, verbose_name='验证码类型')
    send_time = models.DateField(default=datetime.now, verbose_name='发送时间')


    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "code: {} | email: {}".format(self.code, self.email)



class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%m', verbose_name='轮播图')
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name="轮播图播放顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")


    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

