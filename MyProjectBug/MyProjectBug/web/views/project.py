from django.http import JsonResponse
from django.shortcuts import render

from web.froms.project import AddProject


def project_list(request):
    usr_obj = request.session.get("usr_id", 0)
    if request.method == "GET":
        if usr_obj:
            form = AddProject(request.GET)
            return render(request,"web/project_list.html",{"form":form})
        return render(request, 'web/index.html')
    elif request.method == "POST":
        if usr_obj:
            form = AddProject(request,request.POST)
            if form.is_valid():
                form.instance.creator = request.tracer.user
                form.save()
                return render(request, "web/project_list.html", {"form": form})
            return JsonResponse({"status":False,"error": form.errors})
        return render(request, 'web/index.html')

