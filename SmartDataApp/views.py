#coding:utf-8
import re
import logging

from captcha.helpers import captcha_image_url
import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth import authenticate, login as auth_login
from django.core import serializers
from captcha.models import CaptchaStore

from SmartDataApp.forms import UserForm
from SmartDataApp.models import Picture, ProfileDetail


def random_captcha():
    response_data = {}
    response_data['cptch_key'] = CaptchaStore.generate_key()
    response_data['cptch_image'] = captcha_image_url(response_data['cptch_key'])
    return response_data


def generate_captcha(request):
    response_data = random_captcha()
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


def index(request):
    if request.user.is_authenticated():
        return render_to_response('index.html', {'user': request.user})
    else:
        return render_to_response('index.html')

@login_required
def own_information(request):
    profile=ProfileDetail.objects.get(profile=request.user)
    if profile :
        return render_to_response('own_information.html',{'user': request.user ,'profile':profile})
    else :
         return render_to_response('index.html')

@login_required
def dashboard(request):
    return render_to_response('dashboard.html', {
        'username': request.user.username
    })


def multi_response(flag, success, info, template):
    if flag:
        response_data = {'success': success, 'info': info}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        response_data = {'success': success, 'info': info}
        return render_to_response(template, response_data)


@transaction.atomic
@csrf_exempt
def register_old(request):
    if request.method == 'GET':
        response_data = {'success': True}
        response_data.update(csrf(request))
        return render_to_response('register_old.html', response_data)
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
                return multi_response(flag, False, '密码长度为6-15位数字或字母', 'register_old.html')
            if len(User.objects.filter(username=username)) > 0:
                return multi_response(flag, False, '该用户名已经存在', 'register_old.html')
            if len(User.objects.filter(email=email)) > 0:
                return multi_response(flag, False, '该邮箱已经存在', 'register_old.html')
            user = User.objects.get_or_create(username=username)[0]
            if password:
                user.password = make_password(password, 'md5')
            if email:
                user.email = email
            user.save()
            logging.info("user %s, userid %s register success" % (username, user.id))
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
        return redirect(dashboard)


@transaction.atomic
@csrf_exempt
def new_register(request):
    mobile = False
    if request.META['CONTENT_TYPE'] == 'application/json':
        mobile = True
    if request.method == u'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.data.get('username', None)
            password = form.data.get('password', None)
            email = form.data.get('username', None)
            user = User.objects.get_or_create(username=username)[0]
            user.password = make_password(password, 'md5')
            user.email = email
            user.save()
            phone_number = form.data.get('phone_number', None)
            profile = ProfileDetail.objects.get_or_create(profile=user)[0]
            profile.phone_number = phone_number
            profile.save()
            logging.info("user %s, userid %s register success" % (username, user.id))
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    if mobile:
                        response_data = {'success': True}
                        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                    else:
                        return redirect(dashboard)
                else:
                    return redirect(index)
            else:
                if mobile:
                    response_data = {'success': False}
                    return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': True, 'form': form}
            response_data.update(csrf(request))
            return render_to_response('register_old.html', response_data)
    else:
        form = UserForm()
        response_data = {'success': True, 'form': form}
        response_data.update(csrf(request))
        return render_to_response('register_old.html', response_data)


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def profile(request):
    if request.method == 'GET':
        return render_to_response('profile.html', {
            'username': request.user.username,
            'init': True
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
                        multi_response(flag, True, '密码长度为6-15位数字或字母', 'profile.html')
                    if new_password == new_password_again:
                        user.password = make_password(new_password, 'md5')
                        user.save()
                    else:
                        return render_to_response('profile.html', {
                            'username': user.username,
                            'success': False,
                            'info': '两次密码输入不正确!'
                        })
                else:
                    if flag:
                        response_data = {'success': False, 'info': '密码不正确'}
                        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
                    else:
                        return render_to_response('profile.html', {
                            'username': user.username,
                            'success': False,
                            'info': '密码不正确!'
                        })
            logging.info("user %s, userid %s change password success" % (user.username, user.id))
            if flag:
                response_data = {'success': True, 'info': '密码修改成功!'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                return render_to_response('profile.html', {
                    'username': user.username,
                    'success': True,
                    'info': '密码修改成功!'
                })


@csrf_exempt
def login_old(request):
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
                response_data = {'success': False, 'info': '用户不存在'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                return render_to_response('index_old.html', {"hide": False})


def shine(request):
    user = request.user
    username = user.username if user.id else None
    pictures = list(Picture.objects.all().order_by('-timestamp_add'))
    order = request.GET.get('order', None)
    if order == u'like':
        pictures = list(Picture.objects.all().order_by('-like'))
    elif order == u'keep':
        pictures = list(Picture.objects.all().order_by('-keep'))
    mobile = request.GET.get('mobile', None)
    if mobile:
        pictures = serializers.serialize("json", pictures)
        response_data = {'username': username, 'pictures': pictures, 'user_id': user.id}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    return render_to_response('shine.html', {
        'username': username,
        'pictures': pictures,
        'user': user
    })


@csrf_exempt
@transaction.atomic
@login_required
def ajax_upload_image(request):
    if request.method == 'POST':
        upload_src = request.FILES.get('upload_img', None)
        comment = request.POST.get('introduction', None)
        if upload_src is None:
            response_data = {'success': False, 'info': '上传图片不存在！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        name = upload_src.name
        pic_objects = Picture.objects.filter(title=name)
        if len(pic_objects) > 0:
            response_data = {'success': False, 'info': '图片已存在！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        pic = Picture(author=request.user)
        pic.src = upload_src
        pic.comment = comment
        pic.title = upload_src.name
        pic.save()
        response_data = {'success': True, 'info': '图片上传成功！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        response_data = {'success': False, 'info': '仅接受POST请求！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@login_required
@csrf_exempt
@transaction.atomic
def ajax_like(request, id=None):
    if request.method == 'POST' and id:
        picture = Picture.objects.get(id=id)
        picture.like += 1
        picture.save()
        response_data = {'success': True, 'info': '感谢您喜欢这张图片！', 'like': picture.like}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        response_data = {'success': False, 'info': '仅接受POST请求！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@login_required
@csrf_exempt
@transaction.atomic
def ajax_keep(request, id=None):
    #TODO: like function not completed.
    if request.method == 'POST' and id:
        picture = Picture.objects.get(id=id)
        user = request.user
        profile_detail = ProfileDetail.objects.get_or_create(profile=user)[0]
        if picture not in profile_detail.pictures.all():
            picture.keep += 1
            picture.save()
            profile_detail.pictures.add(picture)
            profile_detail.save()
        response_data = {'success': True, 'info': '感谢您喜欢收藏图片！', 'keep': picture.keep}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        response_data = {'success': False, 'info': '仅接受POST请求！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required
def ajax_delete_picture(request, id=None):
    if request.method == 'POST' and id:
        picture = Picture.objects.get(id=id)
        current_user = request.user
        if current_user == picture.author or current_user.is_staff:
            picture.delete()
            response_data = {'success': True, 'info': '删除成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': True, 'info': '非作者，不能删除！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        response_data = {'success': False, 'info': '仅接受POST请求！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
