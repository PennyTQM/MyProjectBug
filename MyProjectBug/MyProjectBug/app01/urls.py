from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url("login/", views.login),
    url("register/", views.register)

]
app_name = "app01"