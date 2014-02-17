#coding:utf-8
import datetime
from django.http import HttpResponse
import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from SmartDataApp.controller.admin import convert_session_id_to_user, return_error_response, return_404_response
from SmartDataApp.controller.complain import UTC
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail, Community, Express



@csrf_exempt
@login_required(login_url='/login/')
def express(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    communities = Community.objects.all()
    express_get_type = request.GET.get(u'type', None)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    if request.user.is_staff or profile.is_admin:
        obtained_expresses = Express.objects.filter(community=one_community, status=True).order_by('-arrive_time')
        not_obtained_expresses = Express.objects.filter(community=one_community, status=False).order_by('-arrive_time')
        expresses = None
        if express_get_type == 'obtained':
            expresses = obtained_expresses
            btn_style = 1
        elif express_get_type == 'not_obtained':
            expresses = not_obtained_expresses
            btn_style = 2
        else:
            expresses = obtained_expresses
            btn_style = 1
        if communities:
            return render_to_response('admin_express.html',
                                      {'user': request.user,
                                       'communities': communities,
                                       'expresses': expresses,
                                       'btn_style': btn_style,
                                       'is_admin': True, 'community': one_community,
                                       'profile': profile,'change_community': status})
        else:
            return render_to_response('admin_express.html', {
                'show': False,
                'user': request.user,
                'is_admin': False,
                'community': one_community,
                'communities': communities,
                'change_community': status
            })
    else:
        expresses = Express.objects.filter(author=profile).order_by('-arrive_time')
        return render_to_response('user_express.html', {'user': request.user,'profile': profile, 'expresses': expresses,'communities': communities, 'is_admin': False, 'community': one_community,'change_community': status})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def find_user_express(request):
    if request.method != u'POST':
        communities = Community.objects.all()
        if len(communities) > 0:
            return render_to_response('admin_express.html', {'user': request.user, 'communities': communities})
    else:
        community_id = request.POST.get(u'community_id', None)
        building_num = request.POST.get(u'building_num', None)
        room_num = request.POST.get(u'room_num', None)
        community = Community.objects.get(id=community_id)
        profile = ProfileDetail.objects.filter(community=community, floor=building_num, gate_card=room_num)
        if profile:
            community_name = community.title
            response_data = {'success': True, 'community_name': community_name, 'building_num': building_num,
                             'room_num': room_num}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '没有此用户！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def add_user_express(request):
    if request.method != u'POST':
        communities = Community.objects.all()
        if len(communities) > 0:
            return render_to_response('admin_express.html', {'user': request.user, 'communities': communities})
    else:
        community_id = request.POST.get(u'community_id', None)
        building_num = request.POST.get(u'building_num', None)
        room_num = request.POST.get(u'room_num', None)
        community = Community.objects.get(id=community_id)
        profile = ProfileDetail.objects.filter(community=community, floor=building_num, gate_card=room_num)
        if profile:
            express = Express(author=profile[0])
            express.handler = request.user
            express.arrive_time = datetime.datetime.now()
            express.is_read = True
            express.community = community
            express.save()
            response_data = {'success': True, 'info': '添加成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '没有此用户！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def delete_user_express(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        express_array = request.POST.get("selected_express_string", None)
        if express_array:
            list_express = str(express_array).split(",")
            for i in range(len(list_express)):
                express_id = int(list_express[i])
                Express.objects.get(id=express_id).delete()
            response_data = {'success': True, 'info': '删除成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def user_get_express(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        express_array = request.POST.get("selected_express_string", None)
        list_express = str(express_array).split(",")
        for i in range(len(list_express)):
            express_id = int(list_express[i])
            express = Express.objects.get(id=express_id)
            express.status = True
            express.get_time = datetime.datetime.now()
            express.save()
        response_data = {'success': True, 'info': '操作成功！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")



@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def user_self_get_express(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        express_array = request.POST.get("selected_express_string", None)
        express_type = request.POST.get("get_express_type", None)
        get_express_time = request.POST.get("get_express_time", None)
        if express_array:
            list_express = str(express_array).split(",")
            for i in range(len(list_express)):
                express_id = int(list_express[i])
                express = Express.objects.get(id=express_id)
                if express.status:
                    response_data = {'success': False, 'info': '包含已签收快件不可提交'}
                    return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            for i in range(len(list_express)):
                express_id = int(list_express[i])
                express = Express.objects.get(id=express_id)
                express.type = express_type
                if get_express_time != u'header':
                    express.allowable_get_express_time = get_express_time
                express.save()
            response_data = {'success': True, 'info': '提交成功！', 'express_type':express_type}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")



@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def express_response(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        express_array = request.POST.get("selected_express_string", None)
        response_content = request.POST.get("response_content", None)
        selected_radio = request.POST.get("selected_radio", None)
        if express_array:
            list_express = str(express_array).split(",")
            for i in range(len(list_express)):
                express_id = int(list_express[i])
                express = Express.objects.get(id=express_id)
                express.pleased = selected_radio
                express.pleased_reason = response_content
                express.save()
            response_data = {'success': True, 'info': '反馈成功！', }
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@csrf_exempt
def api_get_user_express(request):
    convert_session_id_to_user(request)
    profile = ProfileDetail.objects.filter(profile=request.user)
    expresses = Express.objects.filter(author=profile)
    if len(expresses) > 0:
        paginator = Paginator(expresses, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            expresses_list = paginator.page(page).object_list
        except PageNotAnInteger:
            expresses_list = paginator.page(1)
        except EmptyPage:
            expresses_list = paginator.page(paginator.num_pages)
        express_list = list()
        for express_detail in expresses_list:
                time = express_detail.arrive_time
                arrive_time = time.astimezone(UTC(8))
                if express_detail.get_time:
                    time_get = express_detail.get_time
                    get_time = time_get.astimezone(UTC(8))
                else:
                    get_time = express_detail.get_time
                data = {
                    'id': express_detail.id,
                    'express_author': express_detail.author.profile.username,
                    'get_express_type': express_detail.type,
                    'deal_status': express_detail.status,
                    'pleased': express_detail.pleased,
                    'arrive_time': str(arrive_time).split('.')[0],
                    'get_time': str(get_time).split('.')[0]
                }
                express_list.append(data)
        response_data = {'express_list': express_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False, 'info': '没有快递！'}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')




@csrf_exempt
def api_show_all_express(request):
    convert_session_id_to_user(request)
    community_id = request.GET.get("community_id", None)
    if community_id:
        one_community = Community.objects.get(id=community_id)
    else:
        response_data = {'info': '没有传入小区id', 'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    expresses = Express.objects.filter(community=one_community).order_by('-arrive_time')
    if len(expresses) > 0:
        paginator = Paginator(expresses, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            expresses_list = paginator.page(page).object_list
        except PageNotAnInteger:
            expresses_list = paginator.page(1)
        except EmptyPage:
            expresses_list = paginator.page(paginator.num_pages)
        express_list = list()
        for express_detail in expresses_list:
                arrive_time = express_detail.arrive_time
                arrive_time = arrive_time.astimezone(UTC(8))
                if express_detail.get_time:
                    get_time = express_detail.get_time
                    get_time = get_time.astimezone(UTC(8))
                else:
                    get_time = express_detail.get_time
                data = {
                    'id': express_detail.id,
                    'express_author': express_detail.author.profile.username,
                    'get_express_type': express_detail.type,
                    'deal_status': express_detail.status,
                    'pleased': express_detail.pleased,
                    'arrive_time': str(arrive_time).split('.')[0],
                    'get_time': str(get_time).split('.')[0]
                }
                express_list.append(data)
        response_data = {'express_list': express_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False, 'info': '没有快递！'}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_express_response(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        express_id = data.get("express_id", None)
        response_content = data.get("response_content", None)
        selected_pleased = data.get("selected_pleased", None)
        express =Express.objects.get(id=express_id)
        if express and selected_pleased:
            express.pleased_reason = response_content
            express.pleased = selected_pleased
            express.save()
            response_data = {'success': True, 'info': '反馈成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        else:
            response_data = {'success': False, 'info': '反馈失败！'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        return return_404_response()


@transaction.atomic
@csrf_exempt
def api_user_obtain_express(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        express_id = data .get("express_id", None)
        express_type = data .get("express_type", None)
        allowable_get_express_time = data .get("allowable_get_express_time", None)
        express = Express.objects.get(id=express_id)
        if express:
            express.allowable_get_express_time = allowable_get_express_time
            express.type = express_type
            express.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            return return_404_response()


@transaction.atomic
@csrf_exempt
def api_add_express_record(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        community_id = data.get(u'community_id', None)
        building_num = data.get(u'building_num', None)
        room_num = data.get(u'room_num', None)
        community = Community.objects.get(id=community_id)
        profile = ProfileDetail.objects.filter(community=community, floor=building_num, gate_card=room_num)
        if profile:
            express = Express(author=profile[0])
            express.handler = request.user
            express.arrive_time = datetime.datetime.now()
            express.community = community
            express.save()
            response_data = {'success': True, 'info': '添加成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '添加失败！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_find_inhabitant(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        community_id = data.get(u'community_id', None)
        building_num = data.get(u'building_num', None)
        room_num = data.get(u'room_num', None)
        community = Community.objects.get(id=community_id)
        profile = ProfileDetail.objects.filter(community=community, floor=building_num, gate_card=room_num)
        if profile:
            community_name = community.title
            response_data = {'success': True, 'community_name': community_name, 'building_num': building_num,
                             'room_num': room_num}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '没有此用户！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_express_delete(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        express_array = data.get("express_id_string", None)
        if express_array:
            list_express = str(express_array).split(",")
            for i in range(len(list_express)):
                express_id = int(list_express[i])
                Express.objects.get(id=express_id).delete()
            response_data = {'success': True, 'info': '删除成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_express_complete(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        express_array = data.get("express_id_string", None)
        list_express = str(express_array).split(",")
        for i in range(len(list_express)):
            express_id = int(list_express[i])
            express = Express.objects.get(id=express_id)
            express.status = True
            express.get_time = datetime.datetime.now()
            express.save()
        response_data = {'success': True, 'info': '完成领取！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")



@csrf_exempt
def api_show_express_by_status(request):
    convert_session_id_to_user(request)
    community_id = request.GET.get("community_id", None)
    express_status = request.GET.get("status", None)
    profile = ProfileDetail.objects.get(profile=request.user)
    if community_id:
        one_community = Community.objects.get(id=community_id)
    else:
        response_data = {'info': '没有传入小区id', 'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    if request.user.is_staff:
        if express_status == u'领取':
            expresses = Express.objects.filter(community=one_community, status=True).order_by('-get_time')
        if express_status == u'未领取':
            expresses = Express.objects.filter(community=one_community, status=False).order_by('-arrive_time')
    elif profile.is_admin:
        if express_status == u'领取':
            expresses = Express.objects.filter(community=one_community, status=True).order_by('-get_time')
        if express_status == u'未领取':
            expresses = Express.objects.filter(community=one_community, status=False).order_by('-arrive_time')
    else:
        if express_status == u'领取':
            expresses = Express.objects.filter(community=one_community, status=True, author=profile).order_by('-get_time')
        if express_status == u'未领取':
            expresses = Express.objects.filter(community=one_community, status=False,author=profile).order_by('-arrive_time')
    if len(expresses) > 0:
        paginator = Paginator(expresses, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            expresses_list = paginator.page(page).object_list
        except PageNotAnInteger:
            expresses_list = paginator.page(1)
        except EmptyPage:
            expresses_list = paginator.page(paginator.num_pages)
        express_list = list()
        for express_detail in expresses_list:
                arrive_time = express_detail.arrive_time
                arrive_time = arrive_time.astimezone(UTC(8))
                if express_detail.get_time:
                    get_time = express_detail.get_time
                    get_time = get_time.astimezone(UTC(8))
                else:
                    get_time = express_detail.get_time
                data = {
                    'id': express_detail.id,
                    'express_author': express_detail.author.profile.username,
                    'get_express_type': express_detail.type,
                    'deal_status': express_detail.status,
                    'pleased': express_detail.pleased,
                    'arrive_time': str(arrive_time).split('.')[0],
                    'get_time': str(get_time).split('.')[0]
                }
                express_list.append(data)
        response_data = {'express_list': express_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False, 'info': '没有快递！'}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')

