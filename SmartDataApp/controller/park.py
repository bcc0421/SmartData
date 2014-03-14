#coding:utf-8
import datetime
import sys

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from SmartDataApp.models import ProfileDetail, Park_fee, Community


reload(sys)
sys.setdefaultencoding("utf-8")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def parking_fees(request):
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

        #if all_user_info:
        #    all_user_info = all_user_info
        #    show = True
        #else:
        #    show =False

        return render_to_response('admin_park.html',
                                  {'user': request.user, 'profile': profile, 'communities': communities,
                                   'community': one_community, 'change_community': status,
                                   'all_user_info': all_user_info_list})
    else:
        return render_to_response('park_fees.html',
                                  {'user': request.user, 'profile': profile, 'communities': communities,
                                   'community': one_community, 'change_community': status})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def user_property_verifyParking(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    car_number = request.POST.get('car_number', None)
    if car_number:
        park_fee = Park_fee.objects.filter(author=profile)
        if park_fee:
            park_fee[0].car_number = car_number
            park_fee[0].save()
        else:
            park_fee = Park_fee(author=profile)
            park_fee.car_number = car_number
            park_fee.save()
        return render_to_response('user_car_port.html', {
            'user': request.user,
            'profile': profile,
            'communities': communities,
            'community': one_community,
            'change_community': status,
            'car_number': car_number
        })


def add_months(dt, months):
    targetmonth = months + dt.month
    try:
        dt = dt.replace(year=dt.year + int((targetmonth - 1) / 12), month=((targetmonth - 1) % 12) + 1)
    except:
        dt = dt.replace(year=dt.year + int((targetmonth) / 12), month=(((targetmonth ) % 12) + 1), day=1)
        dt += datetime.timedelta(days=-1)
    return dt


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def property_parking_Order(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    type_parking = request.POST.get('type_parking', None)
    period_parking = request.POST.get('period_parking', None)
    park_fee = Park_fee.objects.get(author=profile)
    park_fee.park_type = str(type_parking)
    park_fee.renewal_fees = int(str(period_parking))
    park_fee.valid_time = add_months(park_fee.valid_time, int(str(period_parking)))
    park_fee.save()
    return render_to_response('park_fee_pay_online.html',
                              {'user': request.user,
                               'profile': profile,
                               'park_fee': park_fee,
                               'communities': communities,
                               'community': one_community,
                               'change_community': status})


