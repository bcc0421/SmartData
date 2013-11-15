#coding:utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.response import Response


def index(request):
    return render_to_response('index.html', {"hide": True})

def profile(request):
    dict = {}
    #dict['hide'] = True
    #dict['update_pwd']=True
    return render_to_response('profile.html')
@transaction.autocommit
@csrf_exempt
def register(request):
    if request.method == 'GET':
        dict = {}
        dict['error'] = False
        dict.update(csrf(request))
        return render_to_response('register.html', dict)
    elif request.method == 'POST':
        email = request.POST.get(u'email', None)
        username = request.POST.get(u'username', None)
        password = request.POST.get(u'password', None)
        if email and username and password:
            if len(User.objects.filter(username=username)) > 0:
                dict = {}
                dict.update(csrf(request))
                dict['error'] = True
                dict['error_msg'] = '该用户名已经存在！'
                return render_to_response('register.html', dict)
            user = User.objects.get_or_create(username=username)[0]
            if password:
                user.password = make_password(password, 'md5')
            if email:
                user.email = email
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                return redirect(index)


@transaction.autocommit
@csrf_exempt
@login_required
def update_profile(request):
    if request.method != 'POST':
        return render_to_response('profile.html')
    else:
        username=request.POST.get(u'username',None)
        present_pwd = request.POST.get(u'present_pwd', None)
        new_pwd = request.POST.get(u'new_pwd', None)
        conf_pwd = request.POST.get(u'conf_pwd', None)
        if new_pwd!=conf_pwd:
            return render_to_response('profile.html', {"hide": True})
        else:
            if len(User.objects.filter(username=username)) > 0:
                if present_pwd and new_pwd and conf_pwd:
                    user = User.objects.get(username=username)
                    if check_password(present_pwd, user.password):
                        user.password =make_password(new_pwd, 'md5')
                        user.save()
                        return render_to_response('profile.html', {"visible": True})
                    else:
                        dict = {}
                        dict['error'] = True
                        dict['error_msg'] = '密码错误！'
                        return render_to_response('profile.html', dict)
            else:
                dict = {}
                dict['error'] = True
                dict['error_msg'] = '该用户名不存在！'
                return render_to_response('profile.html', dict)

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return redirect(index)
    else:
        username = request.POST.get(u'username', None)
        password = request.POST.get(u'password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(dashboard)
        else:
            return render_to_response('index.html', {"hide": False})

def logout(request):
    auth_logout(request)
    return redirect(index)


@login_required
def dashboard(request):
    return render_to_response('dashboard.html', {
        'username': request.user.username
    })