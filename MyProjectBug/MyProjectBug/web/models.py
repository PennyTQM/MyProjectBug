from xml.sax.handler import version

from django.db import models

# Create your models here.
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    """用户信息表"""
    usr_name = models.CharField(verbose_name='用户名', max_length=10)
    usr_phone = models.CharField(verbose_name='手机号', max_length=20,
                                 validators=[RegexValidator(r"\d{11}", '手机号码错误')])
    usr_email = models.EmailField(verbose_name='邮箱', max_length=20)
    usr_pwd = models.CharField(verbose_name='密码', max_length=200)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class PricePolicy(models.Model):
    """价格策略表"""
    category = models.SmallIntegerField(verbose_name="收费类型", choices=(
        (1, "免费版本"),
        (2, "VIP"),
        (3, "其他"),
    ), unique=True, default=1)
    title = models.CharField(verbose_name="标题", max_length=32)
    price = models.PositiveIntegerField(verbose_name="价格/年")
    project_num = models.PositiveIntegerField(verbose_name="项目数")
    project_member = models.PositiveIntegerField(verbose_name="项目成员数")
    project_space = models.PositiveIntegerField(verbose_name="单项目空间")
    per_file_size = models.PositiveIntegerField(verbose_name="单文件大小")
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class Trancaction(models.Model):
    '''交易状态表[订单]'''

    status = models.SmallIntegerField(verbose_name="状态", choices=(
        (1, "待支付"),
        (2, "已支付"),

    ), default=1)

    order = models.IntegerField(verbose_name="订单号", unique=True, primary_key=True, )
    user = models.ForeignKey(verbose_name="用户", to="UserInfo")
    price_policy = models.ForeignKey(verbose_name="价格策略", to="PricePolicy")
    count = models.IntegerField(verbose_name="数量(年)", help_text="0表示无期",default=1)
    price = models.DecimalField(verbose_name="实际支付金额", decimal_places=2, max_digits=10, default=0)

    start_datetime = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name="下单时间", auto_now_add=True)


class Project(models.Model):
    """项目表"""
    name = models.CharField(verbose_name="项目名", max_length=32)
    color = models.SmallIntegerField(verbose_name="颜色", max_length=20, choices=(
        (1, "#DC143C"),
        (2, "#00FA9A"),
        (3, "#FFFF00"),
        (4, "#FF8C00"),
        (5, "#48D1CC"),
        (6, "#C0C0C0"),
    ), default=1)
    desc = models.CharField(verbose_name="项目描述", max_length=500, null=True, blank=True)
    use_space = models.IntegerField(verbose_name="项目已使用空间", default=0)
    star = models.BooleanField(verbose_name="星标", default=False)

    bucket = models.CharField(verbose_name="腾讯对象存储", max_length=128)
    region = models.CharField(verbose_name="腾讯对象存储区域", max_length=32)

    join_count = models.SmallIntegerField(verbose_name="参与人数", default=1)
    creator = models.ForeignKey(verbose_name="创建人", to="UserInfo")
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class ProjectUser(models.Model):
    project = models.ForeignKey(verbose_name="项目", to="Project")

    user = models.ForeignKey(verbose_name="用户", to="UserInfo", related_name="user")
    invitee = models.ForeignKey(verbose_name="邀请人", to="UserInfo", related_name="invitee")
    star = models.BooleanField(verbose_name="星标", default=False)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)