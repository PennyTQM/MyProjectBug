from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
from web import models

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        usr_id = request.session.get('usr_id', 0)
        usr_obj = models.UserInfo.objects.filter(id=usr_id).first()
        request.tracer = usr_obj

        if usr_obj and (request.path.__contains__('login') or request.path.__contains__('register')):
            return HttpResponseRedirect('/web/index')



