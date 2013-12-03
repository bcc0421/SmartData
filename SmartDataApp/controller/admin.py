#coding:utf-8
import re
from captcha.models import CaptchaStore

from django.contrib.auth.hashers import make_password
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from SmartDataApp.models import ProfileDetail, Community
from SmartDataApp.views import index, random_captcha


@transaction.atomic
@csrf_exempt
#@login_required
def register(request):
    if request.method != 'POST':
        communities = Community.objects.all()
        response_data = {
            'success': True,
            'user': request.user,
            'communities': communities
        }
        response_data.update(csrf(request))
        return render_to_response('register.html', response_data)
    else:
        username = request.POST.get(u'username', None)
        password = request.POST.get(u'password', None)
        repeatPwd = request.POST.get(u'repeatPwd', None)
        mobile = request.POST.get(u'mobile', None)
        community_id = request.POST.get(u'community', None)
        is_admin = request.POST.get(u'is_admin', None)
        if len(User.objects.filter(username=username)) > 0:
            response_data = {'username_error': True, 'info': u'用户名已存在', 'user': request.user}
            return render_to_response('register.html', response_data)
        if password != repeatPwd:
            response_data = {'password_error': True, 'info': u'两次密码输入不相同', 'user': request.user}
            return render_to_response('register.html', response_data)
        pattern = re.compile(r'^[a-zA-Z0-9]{6,15}$')
        if not pattern.match(password):
            response_data = {'password_error': True, 'info': u'密码：字母、数字组成，6-15位', 'user': request.user}
            return render_to_response('register.html', response_data)
        pattern = re.compile(r'^(1[0-9][0-9])\d{8}$')
        if not pattern.match(mobile):
            response_data = {'mobile_error': True, 'info': u'请输入正确的手机号码', 'user': request.user}
            return render_to_response('register.html', response_data)
        user = User(username=username)
        user.password = make_password(password, 'md5')
        if is_admin == u'2':
            user.is_staff = True
        user.save()
        profile_detail = ProfileDetail(profile=user)
        profile_detail.phone_number = mobile
        community = Community.objects.get(id=community_id)
        profile_detail.community = community
        profile_detail.is_admin = True if is_admin == u'1' else False
        profile_detail.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
        return redirect(index)


@csrf_exempt
def login(request):
    if request.method != u'POST':
        response_data = random_captcha()
        return render_to_response('login.html', response_data)
    else:
        captcha_list = CaptchaStore.objects.filter(hashkey=request.POST.get(u'cptch_key', None))
        if len(captcha_list) == 0:
            response_data = random_captcha()
            response_data['captcha_info'] = u'验证码不正确.'
            return render_to_response('login.html', response_data)
        result = captcha_list[0].response
        verify_code = request.POST.get(u'verify_code', None)
        if result != verify_code:
            response_data = random_captcha()
            response_data['captcha_info'] = u'验证码不正确.'
            return render_to_response('login.html', response_data)
        username = request.POST.get(u'username', None)
        password = request.POST.get(u'password', None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                if request.POST.get(u'remember_me'):
                    request.session.set_expiry(0)
                return redirect(index)
            else:
                response_data = random_captcha()
                response_data['password_info'] = u'手机号码、账号或密码错误.'
                return render_to_response('login.html', response_data)


def logout(request):
    auth_logout(request)
    return redirect(index)
