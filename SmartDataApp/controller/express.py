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
from SmartDataApp.models import Complaints
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail, Community, Express


@csrf_exempt
@login_required(login_url='/login/')
def express(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    if request.user.is_staff or profile.is_admin:
        communities = Community.objects.all()
        expresses = Express.objects.all()
        if communities and express:
            return render_to_response('admin_express.html',
                                      {'user': request.user, 'communities': communities, 'expresses': expresses})
        else:
            return render_to_response('admin_express.html', {
                'show': False,
                'user': request.user,
                'is_admin': False
            })
    else:
        return render_to_response('complains.html', {'user': request.user})


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
            express.arrive_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
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
            express.save()
        response_data = {'success': True, 'info': '操作成功！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
