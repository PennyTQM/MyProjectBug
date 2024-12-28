from traceback import print_tb

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect



def index(request):
    if request.method == "GET":
        usr_obj = request.session.get("usr_id", 0)
        if usr_obj:
            return render(request,'web/index.html')
    return render(request, 'web/index.html')


def logout(request):
    request.session.clear()
    return redirect("web:index")






