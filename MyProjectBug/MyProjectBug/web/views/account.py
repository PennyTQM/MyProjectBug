from django.contrib.sites import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from web.froms.account import RgeisterModelForm, SendSmsForm, LoginSmsFrom, LoginFrom
from django_redis import get_redis_connection
from utils.captcha import generate_captcha
from utils.encrypt import md5
from web.models import UserInfo


def register(request):
    if request.method == "GET":
        form = RgeisterModelForm(request.GET)
        return render(request, 'web/register.html', {'form': form, })
    elif request.method == "POST":
        form = RgeisterModelForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                "status": True,
                "data": "/web/index/"
            })
        return JsonResponse({
            "status": False,
            "error": form.errors
        })


def send_sms(request):
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({"status": False, 'error': form.errors})


def login_sms(request):
    if request.method == "GET":
        form = LoginSmsFrom()
        return render(request, 'web/login_sms.html', {'form': form, })

    if request.method == "POST":
        form = LoginSmsFrom(request.POST)
        if form.is_valid():
            usr_id = form.cleaned_data['usr_id']
            request.session["usr_id"] = usr_id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return JsonResponse({'status': True, "data": "index"}, )
        return JsonResponse({"status": False, "error": form.errors})


def login(request):
    if request.method == "GET":
        form = LoginFrom(request)
        return render(request, 'web/login.html', {'form': form, })
    if request.method == "POST":
        form = LoginFrom(request, data=request.POST)

        if form.is_valid():

            phone_email = form.cleaned_data["phone_email"]
            usr_pwd = form.cleaned_data["usr_pwd"]
            usr_obj = UserInfo.objects.filter(Q(usr_phone=phone_email) | Q(usr_email=phone_email)).filter(
                usr_pwd=usr_pwd).first()

            if usr_obj:
                usr_id = usr_obj.id
                request.session["usr_id"] = usr_id
                request.session.set_expiry(60 * 60 * 24 * 14)
                print("SUCCESS!!!!")
                return redirect("web:index")
            form.add_error("phone_email", "用户名密码错误")
            print("form,",form.errors)
        return render(request, "web/login.html", {"form": form}, )


def get_code(request):
    code, img = generate_captcha()
    print("code:", code)
    request.session['img_code'] = code.upper()
    request.session.set_expiry(60)
    import io
    img_bytes_arry = io.BytesIO()
    img.save(img_bytes_arry, format="JPEG")
    return HttpResponse(img_bytes_arry.getvalue(), content_type="image/jpeg")


