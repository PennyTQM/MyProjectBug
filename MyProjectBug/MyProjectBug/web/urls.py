from django.conf.urls import url, include

from .views import account, index, project

urlpatterns = [

    url(r"register/$", account.register, name="register"),
    url(r"send/sms/$", account.send_sms, name="send_sms"),
    url(r"login/sms$", account.login_sms, name="login_sms"),
    url(r"login/$", account.login, name="login"),
    url(r"getcode/$", account.get_code, name="get_code"),
    url(r"index/$", index.index, name="index"),

    url(r"logout/$", index.logout, name="logout"),
    # 项目管理相关
    url(r"project/list/$", project.project_list, name="project_list"),

]
app_name = "web"
