from django import forms
from django.core.exceptions import ValidationError
from web.views.BootStrip import BootStripFrom
from web.models import Project


class AddProject(BootStripFrom, forms.ModelForm):
    c = [
        (1, "#DC143C"),
        (2, "#00FA9A"),
        (3, "#FFFF00"),
        (4, "#FF8C00"),
        (5, "#48D1CC"),
        (6, "#C0C0C0"),
    ]
    name = forms.CharField(label="项目名", max_length=32, min_length=5, error_messages={
        'min_length': "项目名称不得小于5个字",
        'max_length': "项目名称不得多余20个字"

    }, )

    # color = forms.ChoiceField(label="卡片背景色", choices=c)

    color = forms.ChoiceField(label="卡片背景色", choices=c)

    desc = forms.CharField(label="项目描述", max_length=500, widget=forms.Textarea, error_messages={
        "required ": "不能为空",
        "max_length ": "项目描述最多500个字"
    })

    class Meta:
        model = Project
        fields = ['name', 'color', 'desc']
        widgets = {
            "color": forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


    def clean_pro_name(self):
        pro_name = self.cleaned_data['name']
        exists = Project.objects.filter(pro_name=pro_name).exists()
        if exists:
            raise ValidationError("项目名称已经存在")
        return pro_name

    def clean_name(self):
        name = self.cleaned_data['name']
        exists = Project.objects.filter(name=name, creator=self.request.tracer.user).exists()
        if exists:
            raise ValidationError("项目名已经存在")


        counts = Project.objects.filter(creator=self.request.tracer.user).count()
        if counts >=self.request.tracer.price_policy.project_num:
            raise  ValidationError("权限不足，请开通vip创建更多项目")
        return name




