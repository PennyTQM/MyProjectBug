import random
from ensurepip import bootstrap

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from django.template.context_processors import request

from utils import encrypt
from web.views.BootStrip import BootStripFrom

# from views.account import send_sms
from web import models

from django_redis import get_redis_connection


class RgeisterModelForm(BootStripFrom, forms.ModelForm):
    usr_pwd = forms.CharField(label='密码',
                              min_length=8,
                              max_length=20,
                              error_messages={
                                  'min_length': "密码长度不能小于8个字符",
                                  'max_length': "密码长度不能大于20个字符"
                              },
                              widget=forms.PasswordInput())
    pwd_again = forms.CharField(label='密码',
                                min_length=8,
                                max_length=20,
                                error_messages={
                                    'min_length': "密码长度不能小于8个字符",
                                    'max_length': "密码长度不能大于20个字符"
                                },
                                widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['usr_name', 'usr_email', 'usr_pwd', 'pwd_again', 'usr_phone', 'code']  # 钩子函数会按照顺序验证列表中的字段

    def clean_usr_name(self):
        username = self.cleaned_data['usr_name']
        exist = models.UserInfo.objects.filter(usr_name=username)
        if exist:
            raise ValidationError('用户名已经存在')
        return username

    def clean_usr_email(self):
        email = self.cleaned_data['usr_email']
        exist = models.UserInfo.objects.filter(usr_email=email)
        if exist:
            raise ValidationError('邮箱已存在')
        return email

    def clean_usr_pwd(self):
        password = self.cleaned_data['usr_pwd']
        return encrypt.md5(password)

    def clean_pwd_again(self):
        pwd_again = self.cleaned_data['pwd_again']
        usr_pwd = self.cleaned_data['usr_pwd']
        if encrypt.md5(pwd_again) != usr_pwd:
            raise ValidationError('两次密码不一致')
        return pwd_again

    def clean_usr_phone(self):
        usr_phone = self.cleaned_data['usr_phone']
        exist = models.UserInfo.objects.filter(usr_phone=usr_phone)
        if exist:
            raise ValidationError("手机号已经注册过")
        return usr_phone

    def clean_code(self):
        code = self.cleaned_data['code']
        usr_phone = self.cleaned_data.get('usr_phone')
        if not usr_phone:
            return code
        conn = get_redis_connection("default")
        redis_code = conn.get(usr_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送请重新发送')

        if code.strip() != redis_code.decode('utf8'):
            raise ValidationError("验证码错误，请重新输入")
        return code


class SendSmsForm(forms.Form):
    usr_phone = forms.CharField(label='手机号',
                                validators=[RegexValidator(r"\d{11}", '手机号码错误'), ])

    def __init__(self, request, *args, **kwargs):
        super(SendSmsForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_usr_phone(self):
        usr_phone = self.cleaned_data["usr_phone"]

        exists = models.UserInfo.objects.filter(usr_phone=usr_phone).exists()
        # template_id = settings.TENCENT_SMS_TEMPLATE
        # if not template_id:
        #     raise ValidationError("模板错误")
        tpl = self.request.GET.get("tpl")
        if tpl == "register":
            if exists:
                raise ValidationError("该手机号已经注册")
        else:
            if not exists:
                raise ValidationError("手机号未注册")

        code = random.randint(100000, 999999)
        # sms = send_sms(usr_phone, template_id, [code, ])
        sms = dict()
        sms['code'] = 0
        sms['errmsg'] = "验证码发送失败"

        if sms['code'] != 0:
            raise ValidationError(f"短信发送失败：{sms['errmsg']}")
        conn = get_redis_connection(alias="default")
        conn.set(usr_phone, code, ex=60)
        print("验证码是：", conn.get(usr_phone).decode('utf8'))
        return usr_phone


class LoginSmsFrom(BootStripFrom, forms.Form):
    usr_phone = forms.CharField(label='手机号',
                                validators=[RegexValidator(r"\d{11}", '手机号码错误'), ])

    code = forms.CharField(label='验证码')

    def clean_usr_phone(self):
        usr_phone = self.cleaned_data["usr_phone"]
        user_info = models.UserInfo.objects.filter(usr_phone=usr_phone).first()
        if not user_info:
            raise ValidationError("手机号码不存在")
        return user_info

    def clean_code(self):
        code = self.cleaned_data["code"]
        usr_obj = self.cleaned_data.get("usr_phone")
        if not usr_obj:
            return code
        conn = get_redis_connection("default")
        redis_code = conn.get(usr_obj.usr_phone)
        if not redis_code:
            raise ValidationError("验证码失效/验证码不存在")
        if code.strip() != redis_code.decode('utf8'):
            raise ValidationError("验证码输入错误")
        return code


class LoginFrom(BootStripFrom, forms.Form):
    phone_email = forms.CharField(label="用户名或者邮箱")
    usr_pwd = forms.CharField(label="密码", widget=forms.PasswordInput())
    code = forms.CharField(label="验证码")

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_usr_pwd(self):
        usr_pwd = self.cleaned_data["usr_pwd"]
        return encrypt.md5(usr_pwd)

    def clean_code(self):
        code = self.cleaned_data["code"]
        print(self.request)
        session_code = self.request.session.get("img_code", 0)
        if session_code == 0:
            raise ValidationError("验证码失效，请重新获取")
        if code.upper() != session_code:
            raise ValidationError("验证码错误，请重输入")
        return code.strip()





