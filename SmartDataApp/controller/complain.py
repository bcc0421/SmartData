#coding:utf-8
import datetime
import json
from urllib import unquote
from django.http import HttpResponse, HttpRequest
import simplejson
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
#from SmartDataApp.controller.admin import convert_session_id_to_user
from SmartDataApp.controller.admin import convert_session_id_to_user
from SmartDataApp.models import Complaints, Repair
from SmartDataApp.pusher.Channel import Channel
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail, Community
import hashlib

apiKey = "xS8MeH5f4vfgTukMcB2Bo6Ea"
secretKey = "chcxUOTIvBkItk91bXbXxQw5VSAaYhBb"

class UTC(datetime.tzinfo):
    def __init__(self,offset = 0):
        self._offset = offset

    def utcoffset(self, dt):
        return datetime.timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return datetime.timedelta(hours=self._offset)


def return_error_response():
    response_data = {'error': 'Just support POST method.'}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


def return_404_response():
    return HttpResponse('', content_type='application/json', status=404)


@csrf_exempt
@login_required(login_url='/login/')
def complain(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    deal_status = request.GET.get("deal_status", None)
    if request.user.is_staff:
        if deal_status == u'1':
            complains = Complaints.objects.filter(community=one_community, status=1).order_by('-timestamp')
            btn_status = 1
        elif deal_status == u'2':
            complains = Complaints.objects.filter(community=one_community, status=2).order_by('-timestamp')
            btn_status = 2
        elif deal_status == u'3':
            complains = Complaints.objects.filter(community=one_community, status=3).order_by('-timestamp')
            btn_status = 3
        else:
            complains = Complaints.objects.filter(community=one_community, status=1).order_by('-timestamp')
            btn_status = 1
        deal_person_list = ProfileDetail.objects.filter(is_admin=True, community=one_community)
        if len(complains) > 0:
            paginator = Paginator(complains, 4)
            page = request.GET.get('page')
            try:
                complains_list = paginator.page(page)
            except PageNotAnInteger:
                complains_list = paginator.page(1)
            except EmptyPage:
                complains_list = paginator.page(paginator.num_pages)
            return render_to_response('admin_complains.html', {
                'complains': complains_list,
                'btn_style': btn_status,
                'show': True,
                'community': one_community,
                'change_community': status,
                'user': request.user,
                'deal_person_list': deal_person_list,
                'communities': communities,
                'profile': profile,
                'is_admin': False
            })
        else:
            return render_to_response('admin_complains.html', {
                'show': False,
                'user': request.user,
                'deal_person_list': deal_person_list,
                'community': one_community,
                'communities': communities,
                'change_community': status,
                'profile': profile,
                'is_admin': False
            })
    elif profile.is_admin:
        if deal_status == u'2':
            complains = Complaints.objects.filter(handler=request.user, status=2).order_by('-timestamp')
            btn_status = 2
        elif deal_status == u'3':
            complains = Complaints.objects.filter(handler=request.user, status=3).order_by('-timestamp')
            btn_status = 3
        else:
            complains = Complaints.objects.filter(handler=request.user, status=2).order_by('-timestamp')
            btn_status = 2
        if len(complains) > 0:
            paginator = Paginator(complains, 4)
            page = request.GET.get('page')
            try:
                complains_list = paginator.page(page)
            except PageNotAnInteger:
                complains_list = paginator.page(1)
            except EmptyPage:
                complains_list = paginator.page(paginator.num_pages)
            return render_to_response('worker_complains.html', {
                'complains': complains_list,
                'btn_style': btn_status,
                'show': True,
                'profile': profile,
                'communities': communities,
                'community': one_community,
                'change_community': status,
                'user': request.user,
                'is_admin': True
            })
        else:
            return render_to_response('worker_complains.html', {
                'show': False,
                'communities': communities,
                'profile': profile,
                'community': one_community,
                'change_community': status,
                'user': request.user,
                'is_admin': True
            })
    else:
        return render_to_response('complains.html',
                                  {'user': request.user, 'profile': profile, 'communities': communities,
                                   'community': one_community, 'change_community': status})


@transaction.atomic
@csrf_exempt
def complain_create(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        communities = Community.objects.all()
        complain_content = request.POST.get('content', None)
        complain_type = request.POST.get('category', None)
        upload__complain_src = request.FILES.get('upload_complain_img', None)
        #complain_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        complain_time = datetime.datetime.now()
        profile = ProfileDetail.objects.get(profile=request.user)
        if complain_content or complain_type:
            complain = Complaints()
            complain.content = complain_content
            complain.timestamp = complain_time
            complain.status = 1
            complain.author = request.user.username
            complain.author_detail = profile
            complain.type = complain_type
            complain.community = profile.community
            complain.is_admin_read = True
            if upload__complain_src:
                complain.src = upload__complain_src
            complain.save()
            return render_to_response('complain_success.html',
                                      {'user': request.user, 'communities': communities, 'profile': profile,
                                       'change_community': 2})
        else:
            return render_to_response('complains.html',
                                      {'user': request.user, 'communities': communities, 'profile': profile,
                                       'change_community': 2})


def push_message(description, handler_detail, title):
    c = Channel(apiKey, secretKey)
    push_type = 1
    optional = dict()
    #optional[Channel.USER_ID] = handler_detail.device_user_id
    #optional[Channel.USER_ID] = '665778416804465913'
    optional[Channel.USER_ID] = '665778416804465913'
    optional[Channel.CHANNEL_ID] = '4617656892525519033'
    #optional[Channel.CHANNEL_ID] = '4617656892525519033'
    #optional[Channel.CHANNEL_ID] = handler_detail.device_chanel_id
    #推送通知类型
    optional[Channel.DEVICE_TYPE] = 4
    optional[Channel.MESSAGE_TYPE] = 1
    optional['phone_type'] = handler_detail.device_type
    message_key = hashlib.md5(str(datetime.datetime.now())).hexdigest()
    message = "{" \
              " 'title': '" + title + "', " \
                                      "'description': '" + description + "'" \
                                                                         "}"
    c.pushMessage(push_type, message, message_key, optional)


@transaction.atomic
@csrf_exempt
def complain_deal(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_array = request.POST.get("selected_complain_string", None)
        #handler_array = request.POST.get("selected_handler_string", None)
        deal_person_id = request.POST.get("deal_person_id", None)
        if complain_array and deal_person_id:
            list_complain_ = str(complain_array).split(",")
            #deal_person_id = str(handler_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                complain = Complaints.objects.get(id=com_id)
                complain.is_read = True
                complain.is_worker_read = True
                complain.status = 2
                user_obj = User.objects.get(id=deal_person_id)
                if user_obj:
                    complain.handler = user_obj
                complain.save()
            handler_detail = ProfileDetail.objects.get(profile=user_obj)
            title = 'title'
            description = 'description'
            if handler_detail.device_user_id and handler_detail.device_chanel_id and handler_detail.device_type:
                push_message(description, handler_detail, title)
                response_data = {'success': True, 'info': '授权成功并推送消息至处理人！'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                response_data = {'success': True, 'info': '授权成功,消息推送失败！'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def complain_delete(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_array = request.POST.get("selected_complain_string", None)
        if complain_array:
            list_complain_ = str(complain_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                Complaints.objects.get(id=com_id).delete()
            response_data = {'success': True, 'info': '删除成功'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")

@transaction.atomic
@csrf_exempt
def complain_complete(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_array = request.POST.get("selected_complain_string", None)
        if complain_array:
            list_complain_ = str(complain_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                complain = Complaints.objects.get(id=com_id)
                complain.status = 3
                complain.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def own_complain(request):
    start_time = request.POST.get('start_time', None)
    end_time = request.POST.get('end_time', None)
    if start_time and end_time:
        complains = Complaints.objects.filter(author=request.user.username, timestamp__range=[start_time, end_time])
    else:
        complains = Complaints.objects.filter(author=request.user.username)
    profile = ProfileDetail.objects.get(profile=request.user)
    if len(complains) > 0:
        paginator = Paginator(complains, 7)
        page = request.GET.get('page')
        try:
            complains_list = paginator.page(page)
        except PageNotAnInteger:
            complains_list = paginator.page(1)
        except EmptyPage:
            complains_list = paginator.page(paginator.num_pages)
        return render_to_response('own_complain.html', {
            'complains': complains_list,
            'user': request.user,
            'profile': profile,
            'change_community': 2,
            'show': True
        })
    return render_to_response('own_complain.html',
                              {'show': False, 'user': request.user, 'profile': profile, 'change_community': 2})


@transaction.atomic
@csrf_exempt
@login_required
def complain_response(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_id = request.POST.get("complain_id", None)
        response_content = request.POST.get("response_content", None)
        selected_pleased = request.POST.get("selected_radio", None)
        profile = ProfileDetail.objects.get(profile=request.user)
        complain = Complaints.objects.get(id=complain_id)
        if complain:
            complain.pleased_reason = response_content
            complain.pleased = selected_pleased
            complain.save()
            response_data = {'success': True, 'info': '评论成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            return render_to_response('own_complain.html', {'show': True, 'user': request.user, 'profile': profile})


@csrf_exempt
def show_image_detail(request, id):
    if request.method != u'GET':
        return redirect(index)
    else:
        type = request.GET.get("type", None)
        if type == 'complain':
            complain = Complaints.objects.get(id=id)
            if complain:
                return render_to_response('complain_img_detail.html', {
                    'complain': complain
                })
            else:
                return return_404_response()
        elif type == 'repair':
            repair = Repair.objects.get(id=id)
            if repair:
                return render_to_response('repair_img_detail.html', {
                    'repair': repair
                })
            else:
                return return_404_response()


@transaction.atomic
@csrf_exempt
def api_complain_create(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    else:
        complain_content = request.POST.get('content', None)
        complain_type = request.POST.get('category', None)

        upload__complain_src = request.FILES.get('upload_complain_img', None)
        #complain_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        complain_time = datetime.datetime.now()
        profile = ProfileDetail.objects.get(profile=request.user)
        if complain_content or complain_type:
            complain = Complaints(author=request.user.username)
            complain.content = complain_content
            complain.author_detail = profile
            complain.timestamp = complain_time
            complain.type = complain_type
            complain.is_admin_read = True
            complain.community = profile.community
            if upload__complain_src:
                complain.src = upload__complain_src
            complain.save()
            return HttpResponse(simplejson.dumps({'error': False, 'info': u'投诉创建成功'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'error': True, 'info': u'投诉创建失败'}), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_complain_response(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        complain_id = data.get("complain_id", None)
        response_content = data.get("response_content", None)
        selected_pleased = data.get("selected_pleased", None)
        complain = Complaints.objects.get(id=complain_id)
        if complain and selected_pleased:
            complain.pleased_reason = response_content
            complain.pleased = selected_pleased
            complain.save()
            response_data = {'success': True, 'info': '反馈成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        else:
            response_data = {'success': False, 'info': '反馈失败！'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        return return_404_response()


@transaction.atomic
@csrf_exempt
def api_own_complain(request):
    convert_session_id_to_user(request)
    complains = Complaints.objects.filter(author=request.user.username)
    if len(complains) > 0:
        paginator = Paginator(complains, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            complains_list = paginator.page(page).object_list
        except PageNotAnInteger:
            complains_list = paginator.page(1)
        except EmptyPage:
            complains_list = paginator.page(paginator.num_pages)
        complain_list = list()
        for complain_detail in complains_list:
            time = complain_detail.timestamp
            local = time.astimezone(UTC(8))
            data = {
                'id': complain_detail.id,
                'complain_author': complain_detail.author,
                'author_community': complain_detail.community.title,
                'author_floor': complain_detail.author_detail.floor,
                'author_room': complain_detail.author_detail.gate_card,
                'content': complain_detail.content,
                'type': complain_detail.type,
                'deal_status': complain_detail.status,
                'pleased': complain_detail.pleased,
                'src': complain_detail.src.name,
                'time': str(local).split('.')[0],
                'handler': str(complain_detail.handler)
            }
            complain_list.append(data)
        response_data = {'complain_list': complain_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_complain_deal(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        complain_array = data.get("complains_id_string", None)
        deal_person_id = data.get("deal_person_id", None)
        title = 'title'
        description = 'description'
        if complain_array and deal_person_id:
            list_complain_ = str(complain_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                complain = Complaints.objects.get(id=com_id)
                complain.status = 2
                complain.is_worker_read = True
                complain.is_read = True
                user_obj = User.objects.get(id=deal_person_id)
                if user_obj:
                    complain.handler = user_obj
                complain.save()
            handler_detail = ProfileDetail.objects.get(profile=user_obj)
            if handler_detail.device_user_id and handler_detail.device_chanel_id and handler_detail.device_type:
                push_message(description, handler_detail, title)
                response_data = {'success': True, 'info': u'授权成功，并推送消息至处理人！'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                response_data = {'success': True, 'info': u'授权成功，推送消息失败！'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': u'请选择要处理的投诉'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_complain_complete(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        complain_array = data.get("complains_id_string", None)
        if complain_array:
            list_complain_ = str(complain_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                complain = Complaints.objects.get(id=com_id)
                complain.status = 3
                complain.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_show_all_complains(request):
    convert_session_id_to_user(request)
    community_id = request.GET.get("community_id", None)
    if community_id:
        community = Community.objects.get(id=community_id)
    else:
        response_data = {'info': '没有传入小区id', 'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    complains = Complaints.objects.filter(community=community).order_by('-timestamp')
    if len(complains) > 0:
        paginator = Paginator(complains, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            complains_list = paginator.page(page).object_list
        except PageNotAnInteger:
            complains_list = paginator.page(1)
        except EmptyPage:
            complains_list = paginator.page(paginator.num_pages)
        complain_list = list()
        for complain_detail in complains_list:
            time = complain_detail.timestamp
            local = time.astimezone(UTC(8))
            data = {
                'id': complain_detail.id,
                'complain_author': complain_detail.author,
                'author_community': complain_detail.community.title,
                'author_floor': complain_detail.author_detail.floor,
                'author_room': complain_detail.author_detail.gate_card,
                'content': complain_detail.content,
                'type': complain_detail.type,
                'deal_status': complain_detail.status,
                'pleased': complain_detail.pleased,
                'src': complain_detail.src.name,
                'time': str(local).split('.')[0],
                'handler': str(complain_detail.handler)
            }
            complain_list.append(data)
        response_data = {'complains_list': complain_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False, 'info': '该小区没有投诉'}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_show_complains_by_status(request):
    convert_session_id_to_user(request)
    community_id = request.GET.get("community_id", None)
    complains_status = request.GET.get("status", None)
    profile = ProfileDetail.objects.get(profile=request.user)
    if community_id:
        community = Community.objects.get(id=community_id)
    else:
        response_data = {'info': '没有传入小区id', 'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    if request.user.is_staff:
        if complains_status == u'未处理':
            complains = Complaints.objects.filter(community=community, status=1).order_by('-timestamp')
        if complains_status == u'处理中':
            complains = Complaints.objects.filter(community=community, status=2).order_by('-timestamp')
        if complains_status == u'已处理':
            complains = Complaints.objects.filter(community=community, status=3).order_by('-timestamp')
    elif profile.is_admin:
        if complains_status == u'处理中':
            complains = Complaints.objects.filter(community=community, status=2, handler=request.user).order_by(
                '-timestamp')
        if complains_status == u'已处理':
            complains = Complaints.objects.filter(community=community, status=3, handler=request.user).order_by(
                '-timestamp')
    else:
        if complains_status == u'未处理':
            complains = Complaints.objects.filter(community=community, status=1, author=request.user.username).order_by(
                '-timestamp')
        if complains_status == u'处理中':
            complains = Complaints.objects.filter(community=community, status=2, author=request.user.username).order_by(
                '-timestamp')
        if complains_status == u'已处理':
            complains = Complaints.objects.filter(community=community, status=3, author=request.user.username).order_by(
                '-timestamp')
    if len(complains) > 0:
        paginator = Paginator(complains, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            complains_list = paginator.page(page).object_list
        except PageNotAnInteger:
            complains_list = paginator.page(1)
        except EmptyPage:
            complains_list = paginator.page(paginator.num_pages)
        complain_list = list()
        for complain_detail in complains_list:
            time = complain_detail.timestamp
            local = time.astimezone(UTC(8))
            data = {
                'id': complain_detail.id,
                'complain_author': complain_detail.author,
                'author_community': complain_detail.community.title,
                'author_floor': complain_detail.author_detail.floor,
                'author_room': complain_detail.author_detail.gate_card,
                'content': complain_detail.content,
                'type': complain_detail.type,
                'deal_status': complain_detail.status,
                'pleased': complain_detail.pleased,
                'src': complain_detail.src.name,
                'time': str(local).split('.')[0],
                'handler': str(complain_detail.handler)
            }
            complain_list.append(data)
        response_data = {'complains_list': complain_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False, 'info': '没有搜到要找的结果'}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_complain_create_android(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    else:
        complain_content = unquote(str(request.POST.get('content', None)))
        complain_type = unquote(str(request.POST.get('category', None)))
        upload__complain_src = unquote(str(request.FILES.get('upload_complain_img', None)))
        #complain_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        complain_time = datetime.datetime.now()
        profile = ProfileDetail.objects.get(profile=request.user)
        if complain_content or complain_type:
            complain = Complaints(author=request.user.username)
            complain.content = complain_content
            complain.timestamp = complain_time
            complain.type = complain_type
            complain.is_admin_read = True
            complain.community = profile.community
            if upload__complain_src:
                complain.src = upload__complain_src
            complain.save()
            return HttpResponse(simplejson.dumps({'error': False, 'info': u'投诉创建成功'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'error': True, 'info': u'投诉创建失败'}), content_type='application/json')
