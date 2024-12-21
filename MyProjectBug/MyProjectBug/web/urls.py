from django.conf.urls import url, include

from .views import account

urlpatterns = [

    url(r"^register/$", account.register, name="register")

]
app_name = "web"