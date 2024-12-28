# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2024-12-27 08:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.SmallIntegerField(choices=[(1, '免费版本'), (2, 'VIP'), (3, '其他')], default=1, unique=True, verbose_name='收费类型')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('price', models.PositiveIntegerField(verbose_name='价格/年')),
                ('project_num', models.PositiveIntegerField(verbose_name='项目数')),
                ('project_member', models.PositiveIntegerField(verbose_name='项目成员数')),
                ('project_space', models.PositiveIntegerField(verbose_name='单项目空间')),
                ('per_file_size', models.PositiveIntegerField(verbose_name='单文件大小')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='项目名')),
                ('color', models.CharField(choices=[(1, '#DC143C'), (2, '#00FA9A'), (3, '#FFFF00'), (4, '#FF8C00'), (5, '#48D1CC'), (6, '#C0C0C0')], default=1, max_length=20, verbose_name='颜色')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='项目描述')),
                ('use_space', models.IntegerField(default=0, verbose_name='项目已使用空间')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('bucket', models.CharField(max_length=128, verbose_name='腾讯对象存储')),
                ('region', models.CharField(max_length=32, verbose_name='腾讯对象存储区域')),
                ('join_count', models.SmallIntegerField(default=1, verbose_name='参与人数')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Trancaction',
            fields=[
                ('status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '已支付')], default=1, verbose_name='状态')),
                ('order', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='订单号')),
                ('count', models.IntegerField(help_text='0表示无期', verbose_name='数量(年)')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='实际支付金额')),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='下单时间')),
                ('price_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.PricePolicy', verbose_name='价格策略')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usr_name', models.CharField(max_length=10, verbose_name='用户名')),
                ('usr_phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('\\d{11}', '手机号码错误')], verbose_name='手机号')),
                ('usr_email', models.EmailField(max_length=20, verbose_name='邮箱')),
                ('usr_pwd', models.CharField(max_length=200, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.AddField(
            model_name='trancaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='projectuser',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitee', to='web.UserInfo', verbose_name='邀请人'),
        ),
        migrations.AddField(
            model_name='projectuser',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Project', verbose_name='项目'),
        ),
        migrations.AddField(
            model_name='projectuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='web.UserInfo', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.UserInfo', verbose_name='创建人'),
        ),
    ]
