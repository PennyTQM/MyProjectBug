from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from web.froms.account import RgeisterModelForm, SendSmsForm
from django_redis import get_redis_connection

def register(request):
    form = RgeisterModelForm()
    return render(request, 'web/register.html', {'form': form})


def send_sms(request):
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({"status": False,'error': form.errors})
