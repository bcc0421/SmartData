#coding:utf-8
import re

from captcha.models import CaptchaStore
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import simplejson
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from SmartDataApp.models import ProfileDetail, Community
from SmartDataApp.views import index, random_captcha


def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@transaction.atomic
@csrf_exempt
# @login_required
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
        communities = Community.objects.all()
        username = request.POST.get(u'username', None)
        password = request.POST.get(u'password', None)
        repeatPwd = request.POST.get(u'repeatPwd', None)
        mobile = request.POST.get(u'mobile', None)
        email = request.POST.get(u'email', None)
        community_id = request.POST.get(u'community', None)
        is_admin = request.POST.get(u'is_admin', None)
        floor = request.POST.get(u'floor', None)
        gate_card = request.POST.get(u'gate_card', None)
        address = request.POST.get(u'address', None)
        if len(User.objects.filter(username=username)) > 0:
            response_data = {'username_error': True, 'info': u'用户名已存在', 'user': request.user,
                             'communities': communities}
            return render_to_response('register.html', response_data)
        if password != repeatPwd:
            response_data = {'password_error': True, 'info': u'两次密码输入不相同', 'user': request.user,
                             'communities': communities}
            return render_to_response('register.html', response_data)
        pattern = re.compile(r'^[a-zA-Z0-9]{6,15}$')
        if not pattern.match(password):
            response_data = {'password_error': True, 'info': u'密码：字母、数字组成，6-15位', 'user': request.user,
                             'communities': communities}
            return render_to_response('register.html', response_data)
        pattern = re.compile(r'^(1[0-9][0-9])\d{8}$')
        if not pattern.match(mobile):
            response_data = {'mobile_error': True, 'info': u'请输入正确的手机号码', 'user': request.user,
                             'communities': communities}
            return render_to_response('register.html', response_data)
        if not validateEmail(email):
            response_data = {'email_error': True, 'info': u'请输入正确的邮箱地址', 'user': request.user,
                             'communities': communities}
            return render_to_response('register.html', response_data)
        user = User(username=username)
        user.email = email
        user.password = make_password(password, 'md5')
        if is_admin == u'2':
            user.is_staff = True
        user.save()
        profile_detail = ProfileDetail(profile=user)
        profile_detail.phone_number = mobile
        community = Community.objects.get(id=community_id)
        profile_detail.community = community
        profile_detail.floor = floor
        profile_detail.gate_card = gate_card
        profile_detail.address = address
        profile_detail.is_admin = True if is_admin == u'1' else False
        profile_detail.save()
        return redirect(index)


@csrf_exempt
def login(request):
    if request.method != u'POST':
        response_data = random_captcha()
        return render_to_response('login.html', response_data)
    else:
        captcha_list = CaptchaStore.objects.filter(hashkey=request.POST.get(u'cptch_key', None))
        communities = Community.objects.all()
        if len(captcha_list) == 0:
            response_data = random_captcha()
            response_data['communities'] = communities
            response_data['captcha_info'] = u'验证码不正确.'
            return render_to_response('login.html', response_data)
        result = captcha_list[0].response
        verify_code = request.POST.get(u'verify_code', None)
        if result != verify_code:
            response_data = random_captcha()
            response_data['communities'] = communities
            response_data['captcha_info'] = u'验证码不正确.'
            return render_to_response('login.html', response_data)
        username = request.POST.get(u'username', None)
        password = request.POST.get(u'password', None)
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth_login(request, user)
                if not request.POST.get(u'remember_me', None):
                    request.session.set_expiry(0)
                return redirect(index)
            else:
                response_data = random_captcha()
                response_data['communities'] = communities
                response_data['password_info'] = u'手机号码、账号或密码错误.'
                return render_to_response('login.html', response_data)


def logout(request):
    auth_logout(request)
    return redirect(index)


def return_error_response():
    response_data = {'error': 'Just support POST method.'}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


def return_404_response():
    return HttpResponse('', content_type='application/json', status=404)


def convert_session_id_to_user(request):
    try:
        session = Session.objects.get(session_key=request.META['HTTP_SESSIONID'])
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        request.user = user
    except:
        return_404_response()


@csrf_exempt
@transaction.atomic
def api_user_create(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif request.META['CONTENT_TYPE'] == 'application/json':
        data = simplejson.loads(request.body)
        username = data.POST.get(u'username', None)
        password = data.POST.get(u'password', None)
        repeatPwd = data.POST.get(u'repeatPwd', None)
        mobile = data.POST.get(u'mobile', None)
        email = data.POST.get(u'email', None)
        community_id = data.POST.get(u'community', None)
        is_admin = data.POST.get(u'is_admin', None)
        floor = data.POST.get(u'floor', None)
        gate_card = data.POST.get(u'gate_card', None)
        address = data.POST.get(u'address', None)
        if len(User.objects.filter(username=username)) > 0:
            response_data = {'username_error': True, 'info': u'用户名已存在'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        if password != repeatPwd:
            response_data = {'password_error': True, 'info': u'两次密码输入不相同'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        pattern = re.compile(r'^[a-zA-Z0-9]{6,15}$')
        if not pattern.match(password):
            response_data = {'password_error': True, 'info': u'密码：字母、数字组成，6-15位'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        pattern = re.compile(r'^(1[0-9][0-9])\d{8}$')
        if not pattern.match(mobile):
            response_data = {'mobile_error': True, 'info': u'请输入正确的手机号码'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        if not validateEmail(email):
            response_data = {'email_error': True, 'info': u'请输入正确的邮箱地址'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        user = User(username=username)
        user.password = make_password(password, 'md5')
        user.email = email
        if is_admin == u'2':
            user.is_staff = True
        user.save()
        profile_detail = ProfileDetail(profile=user)
        profile_detail.phone_number = mobile
        community = Community.objects.get(id=community_id)
        profile_detail.community = community
        profile_detail.floor = floor
        profile_detail.gate_card = gate_card
        profile_detail.address = address
        profile_detail.is_admin = True if is_admin == u'1' else False
        profile_detail.save()
        return HttpResponse(simplejson.dumps({'info': 'create user successful'}), content_type='application/json')
    else:
        return return_404_response()


@csrf_exempt
def api_user_login(request):
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        username = data.get(u'username', None)
        password = data.get(u'password', None)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth_login(request, user)
            profile = ProfileDetail.objects.get(profile=user)
            if user.is_staff:
                response_data = {'identity': 'admin', 'info': 'login successful'}
                return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
            elif profile.is_admin:
                response_data = {'identity': 'worker', 'info': 'login successful'}
                return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
            else:
                response_data = {'identity': 'resident', 'info': 'login successful'}
                return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'info': 'login failed'}), content_type='application/json')
    else:
        return return_404_response()


@csrf_exempt
@transaction.atomic
def api_user_update(request):
    convert_session_id_to_user(request)

    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        username = data.get(u'username', None)
        mobile = data.get(u'mobile', None)
        email = data.get(u'email', None)
        community_id = data.get(u'community', None)
        floor = data.get(u'floor', None)
        gate_card = data.get(u'gate_card', None)
        address = data.get(u'address', None)
        pattern = re.compile(r'^(1[0-9][0-9])\d{8}$')
        if not pattern.match(mobile):
            response_data = {'mobile_error': True, 'info': u'请输入正确的手机号码'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        if not validateEmail(email):
            response_data = {'email_error': True, 'info': u'请输入正确的邮箱地址'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        user = request.user
        user.email = email
        user.save()
        profile_detail = ProfileDetail.objects.get(profile=user)
        community = Community.objects.get(id=community_id)
        profile_detail.community = community
        profile_detail.floor = floor
        profile_detail.gate_card = gate_card
        profile_detail.address = address
        profile_detail.save()
        return HttpResponse(simplejson.dumps({'info': 'update profile detail successful'}),
                            content_type='application/json')
    else:
        return return_404_response()


@csrf_exempt
@transaction.atomic
def api_user_change_password(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        old_password = data.get(u'old_password', None)
        new_password = data.get(u'new_password', None)
        repeat_password = data.get(u'repeat_password', None)
        user = request.user
        if new_password != repeat_password:
            response_data = {'error': True, 'info': u'两次密码不一致'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        if check_password(old_password, user.password):
            pattern = re.compile('\w{6,15}')
            match = pattern.match(new_password)
            if not match:
                response_data = {'error': True, 'info': u'密码长度为6-15位数字或字母'}
                return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
            else:
                user.password = make_password(new_password, 'md5')
                user.save()
                return HttpResponse(simplejson.dumps({'error': False, 'info': u'密码更新成功'}),
                                    content_type='application/json')
        else:
            response_data = {'error': True, 'info': u'旧密码不正确'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        return return_404_response()


@transaction.atomic
@csrf_exempt
def api_user_delete(request):
    convert_session_id_to_user(request)

    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        pass


@csrf_exempt
def api_user_list(request):
    convert_session_id_to_user(request)

    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        user = request.user
        if not user.is_staff:
            return HttpResponse(simplejson.dumps({'error': True, 'info': u'仅限管理员访问'}), content_type='application/json')
        else:
            profile_detail_list = ProfileDetail.objects.all()
            response_data = list()
            for profile_detail in profile_detail_list:
                data = {
                    'id': profile_detail.profile.id,
                    'username': profile_detail.profile.username,
                    'phone_number': profile_detail.phone_number,
                    'email': profile_detail.profile.email,
                    'community': profile_detail.community.title,
                    'floor': profile_detail.floor,
                    'gate_card': profile_detail.gate_card,
                    'address': profile_detail.address
                }
                response_data.append(data)
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        return return_404_response()


def api_user_logout(request):
    auth_logout(request)
    return HttpResponse(simplejson.dumps({'info': u'成功登出'}), content_type='application/json')


@csrf_exempt
def api_get_worker_list(request):
    convert_session_id_to_user(request)
    community_id = request.GET.get("community_id", None)
    if community_id:
        community = Community.objects.get(id=community_id)
    else:
        response_data = {'info': '没有传入小区id', 'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    deal_person_list = ProfileDetail.objects.filter(is_admin=True, community=community)
    if deal_person_list:
        worker_list = list()
        for profile_detail in deal_person_list:
            data = {
                'id': profile_detail.profile.id,
                'username': profile_detail.profile.username,
                'phone_number': profile_detail.phone_number,
            }
            worker_list.append(data)
        response_data = {'worker_list': worker_list, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse(simplejson.dumps({'success': False}), content_type='application/json')