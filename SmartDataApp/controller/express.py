#coding:utf-8
import datetime
from django.http import HttpResponse
import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from SmartDataApp.controller.admin import convert_session_id_to_user, return_error_response, return_404_response
from SmartDataApp.models import Complaints
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail, Community, Express


@csrf_exempt
@login_required(login_url='/login/')
def express(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    communities = Community.objects.all()
    if request.user.is_staff or profile.is_admin:
        expresses = Express.objects.all().order_by('-arrive_time')
        if communities and express:
            return render_to_response('admin_express.html',
                                      {'user': request.user, 'communities': communities, 'expresses': expresses, 'is_admin': True})
        else:
            return render_to_response('admin_express.html', {
                'show': False,
                'user': request.user,
                'is_admin': False
            })
    else:
        expresses = Express.objects.filter(author=profile).order_by('-arrive_time')
        return render_to_response('admin_express.html', {'user': request.user, 'expresses': expresses, 'is_admin': False})


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
        profile = ProfileDetail.objects.filter(community=community, floor=building_num, gate_card=room_num)[0]
        if profile:
            express = Express(author=profile)
            express.handler = request.user
            express.arrive_time = datetime.datetime.now()
            express.save()
            response_data = {'success': True, 'info': '添加成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '添加失败！'}
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
    expresses = Express.objects.all()
    if len(expresses) > 0:
        paginator = Paginator(expresses, 5)
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
                data = {
                    'id': express_detail.id,
                    'express_author': express_detail.author.profile.username,
                    'get_express_type': express_detail.type,
                    'deal_status': express_detail.status,
                    'pleased': express_detail.pleased,
                    'arrive_time': str(express_detail.arrive_time),
                    'get_time': str(express_detail.get_time)
                }
                express_list.append(data)
        response_data = {'express_list': express_list, 'page_count': page_count}
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
        profile = ProfileDetail.objects.filter(community=community, floor=building_num, gate_card=room_num)[0]
        if profile:
            express = Express(author=profile)
            express.handler = request.user
            express.arrive_time = datetime.datetime.now()
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