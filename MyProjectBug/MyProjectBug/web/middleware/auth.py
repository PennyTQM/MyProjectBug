import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
from web import models

from django.conf import settings

class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.tracer = Tracer()
        usr_id = request.session.get('usr_id', 0)
        usr_obj = models.UserInfo.objects.filter(id=usr_id).first()
        request.tracer.user = usr_obj
        if request.path_info  in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.tracer.user:
            return redirect("login")

        _obj = models.Trancaction.objects.filter(user=usr_obj, status=2).order_by("-create_datetime").first()
        curr_time = datetime.datetime.now()
        if _obj.end_datetime and _obj.end_datetime < curr_time:
            _obj = models.Trancaction.objects.filter(user=usr_obj, status=2).order_by("-id").first()
        request.tracer.price_policy = _obj.price_policy


        # _obj = models.Trancaction.objects.filter(user=usr_obj,status=2).order_by("-id").first()
        # if not _obj:
        #     request.price_policy = models.PricePolicy.objects.filter(category=1).first()
        # else:
        #     current_time = datetime.datetime.now()
        #     if _obj.end_datetime and _obj.end_datetime < current_time:
        #         request.price_policy = models.PricePolicy.objects.filter(category=1).first()
        #     else:
        #         request.price_policy = _obj.price_policy



