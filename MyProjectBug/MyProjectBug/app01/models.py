from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    usr_name = models.CharField(verbose_name='用户名', max_length=10)
    telnumber = models.CharField(verbose_name='手机号', max_length=20,
                                 validators=[RegexValidator(r"^(?:0|86|＋?86)?1\d{9}$", '手机号码错误')])
    use_email = models.EmailField(verbose_name='邮箱', max_length=20)
    usr_pwd = models.CharField(verbose_name='密码', max_length=200)
