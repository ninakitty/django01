from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(choices=(('male', '男'), ('female', '女')), default='female', max_length=6)
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null='', blank='')
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        # ordering = ['name']  # 按照哪个栏目排序

        # def __str__(self):
        #     return '{0}({1})'.format(self.code, self.username)


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=10, verbose_name='验证码类型', choices=(('register', '注册'), ('forget', '忘记密码')))
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

        # def __str__(self):
        #     return self.email


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='static/banner/%Y/%m', verbose_name='轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='位置')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
