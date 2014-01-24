#coding:utf-8
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from SmartDataApp.models import ProfileDetail, Community
from SmartDataApp.views import index, own_information
from django.contrib.sessions.models import Session
def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def update_own_profile(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    communities = Community.objects.all()
    if profile:
        return render_to_response('update_profile.html',
                                  {'user': request.user, 'profile': profile, 'communities': communities})
    else:
        return render_to_response('index.html')


@transaction.atomic
@csrf_exempt
@login_required
def profile_update(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        user = request.user
        communities = Community.objects.all()
        profile_detail = ProfileDetail.objects.get(profile=user)
        new_name = request.POST.get(u'new_name', None)
        new_mobile = request.POST.get(u'new_mobile', None)
        new_email = request.POST.get(u'new_email', None)
        new_building = request.POST.get(u'new_building', None)
        new_room = request.POST.get(u'new_room', None)
        new_address = request.POST.get(u'new_address', None)
        new_community_id = request.POST.get(u'community', None)
        pattern = re.compile(r'^(1[0-9][0-9])\d{8}$')
        if not pattern.match(new_mobile):
            response_data = {'mobile_error': True, 'info': u'请输入正确的手机号码', 'communities': communities,
                             'profile': profile_detail, 'user': user}
            return render_to_response('update_profile.html', response_data)
        if not validateEmail(new_email):
            response_data = {'email_error': True, 'info': u'请输入正确的邮箱地址', 'communities': communities,
                             'profile': profile_detail, 'user': user}
            return render_to_response('update_profile.html', response_data)
        user.email = new_email
        user.username = new_name
        user.save()
        community = Community.objects.get(id=new_community_id)
        profile_detail.community = community
        profile_detail.floor = new_building
        profile_detail.gate_card = new_room
        profile_detail.address = new_address
        profile_detail.save()
        return redirect(own_information)


def update_own_password(request):
    return render_to_response('update_password.html')


@transaction.atomic
@csrf_exempt
@login_required
def update_password(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        old_password = request.POST.get(u'old_password', None)
        new_password = request.POST.get(u'new_password', None)
        repeat_password = request.POST.get(u'repeat_password', None)
        user = request.user
        if new_password != repeat_password:
            response_data = {'error1': True, 'info': u'两次密码不一致'}
            return render_to_response('update_password.html', response_data)
        if check_password(old_password, user.password):
            pattern = re.compile('\w{6,15}')
            match = pattern.match(new_password)
            if not match:
                response_data = {'error2': True, 'info': u'密码长度为6-15位数字或字母'}
                return render_to_response('update_password.html', response_data)
            else:
                user.password = make_password(new_password, 'md5')
                user.save()
                Session.objects.get(session_key=request.META['HTTP_SESSIONID']).delete()
                return redirect(own_information)
        else:
            response_data = {'error3': True, 'info': u'旧密码不正确'}
            return render_to_response('update_password.html', response_data)