#coding:utf-8
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from SmartDataApp.models import Community
from SmartDataApp.views import index

@csrf_exempt
@login_required(login_url='/login/')
def repair(request):
    if not request.user.is_staff:
            return render_to_response('repair.html', {'user': request.user})
