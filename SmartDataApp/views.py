#coding:utf-8
import simplejson as json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def index(request):
    return render_to_response('index.html', {"hide": True})


@transaction.autocommit
@csrf_exempt
def register(request):
    if request.method == 'GET':
        dict = {}
        dict['error'] = False
        dict.update(csrf(request))
        return render_to_response('register.html', dict)
    elif request.method == 'POST':
        if request.META['CONTENT_TYPE'] == 'application/json':
            data = json.loads(request.body)
            email = data.get(u'email', None)
            username = data.get(u'username', None)
            password = data.get(u'password', None)
        else:
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
                else:
                    return redirect(index)
        else:
            return redirect(index)

@transaction.autocommit
@csrf_exempt
@login_required
def profile(request):
    if request.method != 'POST':
        return render_to_response('profile.html', {
            'username': request.user.username,
            'error': False
        })
    else:
        old_password = request.POST.get(u'old_password', None)
        new_password = request.POST.get(u'new_password', None)
        new_password_again = request.POST.get(u'new_password_again', None)
        if old_password and new_password and new_password_again:
            user = request.user
            if old_password:
                if check_password(old_password, user.password):
                    if new_password == new_password_again:
                        user.password = make_password(new_password, 'md5')
                    else:
                        return render_to_response('profile.html', {
                            'username': user.username,
                            'error': True,
                            'error_msg': '两次密码输入不正确!'
                        })
                else:
                    return render_to_response('profile.html', {
                        'username': user.username,
                        'error': True,
                        'error_msg': '密码不正确!'
                    })
            user.save()
            return render_to_response('profile.html', {
                'username': user.username,
                'success': True,
                'success_msg': '密码修改成功!'
            })


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

