from django import forms

from web import models


class RgeisterModelForm(forms.ModelForm):
    usr_pwd = forms.CharField(label='密码', max_length=200, widget=forms.PasswordInput())
    pwd_again = forms.CharField(label='重复密码', max_length=200, widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['usr_name', 'use_email', 'telnumber', 'usr_pwd', 'pwd_again', 'code']

    def __init__(self, *args, **kwargs):
        super(RgeisterModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'
