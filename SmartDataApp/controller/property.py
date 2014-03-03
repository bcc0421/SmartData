#coding:utf-8
import datetime
from decimal import Decimal
from django.utils.timezone import utc
from django.http import HttpResponse
import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from SmartDataApp.controller.admin import convert_session_id_to_user
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail, Housekeeping, Housekeeping_items,Community,Wallet


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def house_pay_fees(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    all_user_info_list = []
    if request.user.is_staff:
        all_user_info = profile.community.profiledetail_set.all()
        for user_info in all_user_info:
            if user_info.profile.is_staff == False and user_info.is_admin == False:
                all_user_info_list.append(user_info)
        return render_to_response('admin_property_fees.html', {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status,'all_user_info': all_user_info_list})

    else:
      return render_to_response('housing_service_fee.html', {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status})




@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def user_pay_property_by_month(request):
    communities = Community.objects.all()
    profile = ProfileDetail.objects.get(profile=request.user)
    return render_to_response('user_pay_property_by_month.html', {'user': request.user, 'communities': communities, 'profile': profile, 'change_community': 2})

@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def user_prepare_pay_fee(request):
    communities = Community.objects.all()
    profile = ProfileDetail.objects.get(profile=request.user)
    return render_to_response('user_prepare_pay_fee.html', {'user': request.user, 'communities': communities, 'profile': profile, 'change_community': 2})

@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def property_user_pay_online(request):
    communities = Community.objects.all()
    profile = ProfileDetail.objects.get(profile=request.user)
    return render_to_response('property_user_pay_online.html',{'user': request.user, 'communities': communities, 'profile': profile, 'change_community': 2})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def property_service(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    if request.user.is_staff:
        return render_to_response('property_service.html', {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status})
    elif profile.is_admin:
       return render_to_response('property_service.html', {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status})
    else:
      return render_to_response('property_service.html', {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def user_recharge(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    return render_to_response('user_recharge.html',
                                  {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status,})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def decide_recharge(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    money_num = request.POST.get('money_num', None)
    money_num = Decimal(str(money_num))
    wallet = Wallet.objects.get_or_create(user_profile=profile)[0]
    wallet.money_sum += money_num
    wallet.save()
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    response_data = {'info': '充值成功', 'success': True}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')