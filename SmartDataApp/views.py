#coding:utf-8
import re

import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def index(request):
    return render_to_response('index.html', {"hide": True})


@transaction.atomic
@csrf_exempt
def register(request):
    if request.method == 'GET':
        response_data = {'error': False}
        response_data.update(csrf(request))
        return render_to_response('register.html', response_data)
    elif request.method == 'POST':
        flag = False
        email, username, password = None, None, None
        if request.META['CONTENT_TYPE'] == 'application/json':
            data = simplejson.loads(request.body)
            email = data.get(u'email', None)
            username = data.get(u'username', None)
            password = data.get(u'password', None)
            flag = True
        else:
            email = request.POST.get(u'email', None)
            username = request.POST.get(u'username', None)
            password = request.POST.get(u'password', None)
        if email and username and password:
            pattern = re.compile('\w{6,15}')
            match = pattern.match(password)
            if not match:
                response_data = {'error': True, 'error_msg': '密码长度为6-15位数字或字母'}
                if flag:
                    return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                else:
                    return render_to_response('register.html', response_data)
            if len(User.objects.filter(username=username)) > 0:
                if flag:
                    response_data = {'success': False, 'error': '该用户名已经存在'}
                    return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                else:
                    response_data = {'error': True, 'error_msg': '该用户名已经存在!'}
                    return render_to_response('register.html', response_data)
            if len(User.objects.filter(email=email)) > 0:
                if flag:
                    response_data = {'success': False, 'error': '该邮箱已经存在'}
                    return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                else:
                    response_data = {'error': True, 'error_msg': '该邮箱已经存在!'}
                    return render_to_response('register.html', response_data)
            user = User.objects.get_or_create(username=username)[0]
            if password:
                user.password = make_password(password, 'md5')
            if email:
                user.email = email
            user.save()
            user = authenticate(username=username, password=password)
            if flag:
                response_data = {'success': True}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                    else:
                        return redirect(index)
        return redirect(index)



@transaction.atomic
@csrf_exempt
@login_required
def profile(request):
    if request.method != 'POST':
        return render_to_response('profile.html', {
            'username': request.user.username,
            'error': False
        })
    elif request.method == 'POST':
        flag = False
        old_password, new_password, new_password_again = None, None, None
        if request.META['CONTENT_TYPE'] == 'application/json':
            data = simplejson.loads(request.body)
            old_password = data.get(u'old_password', None)
            new_password = data.get(u'new_password', None)
            new_password_again = data.get(u'new_password_again', None)
            flag = True
        else:
            old_password = request.POST.get(u'old_password', None)
            new_password = request.POST.get(u'new_password', None)
            new_password_again = request.POST.get(u'new_password_again', None)
        if old_password and new_password and new_password_again:
            user = request.user
            if old_password:
                if check_password(old_password, user.password):
                    pattern = re.compile('\w{6,15}')
                    match = pattern.match(new_password)
                    if not match:
                        response_data = {'error': True, 'error_msg': '密码长度为6-15位数字或字母'}
                        if flag:
                            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                        else:
                            return render_to_response('profile.html', response_data)
                    if new_password == new_password_again:
                        user.password = make_password(new_password, 'md5')
                    else:
                        return render_to_response('profile.html', {
                            'username': user.username,
                            'error': True,
                            'error_msg': '两次密码输入不正确!'
                        })
                else:
                    if flag:
                        response_data = {'success': False, 'error': '密码不正确'}
                        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                    else:
                        return render_to_response('profile.html', {
                            'username': user.username,
                            'error': True,
                            'error_msg': '密码不正确!'
                        })
            user.save()
            if flag:
                response_data = {'success': True}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                return render_to_response('profile.html', {
                    'username': user.username,
                    'success': True,
                    'success_msg': '密码修改成功!'
                })


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return redirect(index)
    elif request.method == 'POST':
        flag = False
        username, password = None, None
        if request.META['CONTENT_TYPE'] == 'application/json':
            data = simplejson.loads(request.body)
            username = data.get(u'username', None)
            password = data.get(u'password', None)
            flag = True
        else:
            username = request.POST.get(u'username', None)
            password = request.POST.get(u'password', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                if flag:
                    response_data = {'success': True, 'user_id': user.id}
                    return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                else:
                    return redirect(dashboard)
        else:
            if flag:

                response_data = {}
                response_data = {'success': False, 'error': '用户不存在'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
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


def shine(request):
    user = request.user
    username = user.username if user.id else None
    return render_to_response('shine.html', {
        'username': username
    })

@csrf_exempt
def ajax_upload_image(request):
    if request.method == 'POST':
        print "123"
        return render_to_response('index.html', {"hide": False})
    else:
        pass
