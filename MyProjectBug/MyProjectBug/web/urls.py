from django.conf.urls import url, include

from .views import account,index

urlpatterns = [

    url(r"^register/$", account.register, name="register"),
    url(r"send/sms/$", account.send_sms, name="send_sms"),
    url(r"login/sms$", account.login_sms, name="login_sms"),
    url(r"login/$", account.login, name="login"),
    url(r"getcode/$", account.get_code, name="get_code"),
    url(r"logout/$", index.logout, name="logout"),

    url(r"index/$", index.index, name="index"),

]
app_name = "web"