import random

from asgiref.timeout import timeout
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings

# from views.account import send_sms
from web import models

from django_redis import get_redis_connection


# from MyProjectBug.utils.tencent import *

class RgeisterModelForm(forms.ModelForm):
    usr_pwd = forms.CharField(label='密码', max_length=200, widget=forms.PasswordInput())
    pwd_again = forms.CharField(label='重复密码', max_length=200, widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['usr_name', 'use_email', 'usr_pwd', 'pwd_again', 'telnumber', 'code']

    def __init__(self, *args, **kwargs):
        super(RgeisterModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'


class SendSmsForm(forms.Form):
    telnumber = forms.CharField(label='手机号',
                                validators=[RegexValidator(r"^1[3589]{1}\d{9}", '手机号码错误'), ])

    def __init__(self, request, *args, **kwargs):
        super(SendSmsForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_telnumber(self):
        telnumber = self.cleaned_data["telnumber"]
        exists = models.UserInfo.objects.filter(telnumber=telnumber).exists()
        # template_id = settings.TENCENT_SMS_TEMPLATE
        # if not template_id:
        #     raise ValidationError("模板错误")
        if exists:
            raise ValidationError("该手机号已经注册")

        code = random.randint(100000, 999999)
        # sms = send_sms(telnumber, template_id, [code, ])
        sms = {}
        sms['code'] = random.randint(0,1)
        sms['errmsg'] = "验证码发送失败"

        if sms['code'] != 0:
            raise ValidationError(f"短信发送失败：{sms['errmsg']}")
        conn = get_redis_connection()
        conn.set(telnumber, code, ex=60)
        return telnumber
