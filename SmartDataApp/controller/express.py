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
from SmartDataApp.models import ProfileDetail,Community




@csrf_exempt
@login_required(login_url='/login/')
def express(request):
        profile = ProfileDetail.objects.get(profile=request.user)
        if request.user.is_staff:
            communities = Community.objects.all()
            if len(communities) > 0:
                return render_to_response('admin_express.html', {'user': request.user, 'communities': communities})
            else:
                return render_to_response('admin_complains.html', {
                    'show': False,
                    'user': request.user,
                    'is_admin': False
                })
        elif profile.is_admin:
            complains = Complaints.objects.filter(handler = request.user)
            if len(complains) > 0:
                return render_to_response('admin_complains.html', {
                    'complains': list(complains),
                    'show': True,
                    'user': request.user,
                    'is_admin': True
                })
            else:
                return render_to_response('admin_complains.html', {
                    'show': False,
                    'user': request.user,
                    'is_admin': True
                })
        else:
            return render_to_response('complains.html', {'user': request.user})

@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def find_user(request):
       if request.method != u'POST':
            communities = Community.objects.all()
            if len(communities) > 0:
                return render_to_response('admin_express.html', {'user': request.user, 'communities': communities})
       else:
            community_id = request.POST.get(u'community_id', None)
            building_num = request.POST.get(u'building_num', None)
            room_num = request.POST.get(u'room_num', None)
            community = Community.objects.get(id=community_id)
            profile = ProfileDetail.objects.filter(community=community ,floor=building_num ,gate_card=room_num)
            if profile:
                community_name = community.title
                response_data = {'success': True, 'community_name': community_name, 'building_num': building_num,'room_num': room_num}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                response_data = {'success': False, 'info': '没有此用户！'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")