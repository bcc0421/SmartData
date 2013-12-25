#coding:utf-8
import datetime
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
from SmartDataApp.models import ProfileDetail, Housekeeping, Housekeeping_items,Community

def return_error_response():
    response_data = {'error': 'Just support POST method.'}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')

def return_404_response():
    return HttpResponse('', content_type='application/json', status=404)

@csrf_exempt
@login_required(login_url='/login/')
def housekeeping(request):
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
            housekeeping = Housekeeping.objects.filter(community=one_community).order_by('-time')
            deal_person_list = ProfileDetail.objects.filter(is_admin=True, community=one_community)
            if len(housekeeping) > 0:
                return render_to_response('admin_housekeeping.html', {
                    'housekeeping': list(housekeeping),
                    'show': True,
                    'user': request.user,
                    'community': one_community,
                    'change_community': status,
                    'profile': profile,
                    'communities': communities,
                    'deal_person_list': deal_person_list,
                    'is_admin': True
                })
            else:
                return render_to_response('admin_housekeeping.html', {
                    'show': False,
                    'user': request.user,
                    'community': one_community,
                    'change_community': status,
                    'communities': communities,
                    'profile': profile,
                    'deal_person_list': deal_person_list
                })
        elif profile.is_admin:
            housekeeping = Housekeeping.objects.filter(handler=request.user)
            if len(housekeeping) > 0:
                return render_to_response('admin_housekeeping.html', {
                    'housekeeping': list(housekeeping),
                    'show': True,
                    'community': one_community,
                    'change_community': status,
                    'profile': profile,
                    'communities': communities,
                    'user': request.user,
                    'is_admin': False
                })
            else:
                return render_to_response('admin_housekeeping.html', {
                    'show': False,
                    'community': one_community,
                    'change_community': status,
                    'profile': profile,
                    'communities': communities,
                    'user': request.user,
                    'is_admin': False

                })
        else:
            housekeeping_items = Housekeeping_items.objects.all()
            if housekeeping_items:
                return render_to_response('housekeeping.html', {'user': request.user, 'communities': communities, 'housekeeping_items': housekeeping_items, 'is_show': True, 'change_community': status,  'community': one_community, 'profile': profile})
            else:
                return render_to_response('housekeeping.html', {'user': request.user, 'communities': communities, 'is_show':False, 'community': one_community, 'change_community': status, 'profile': profile})

@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def manage_housekeeping_item(request):
    items = Housekeeping_items.objects.all()
    if len(items) > 0:
        return render_to_response('manage_housekeeping_item.html', {
            'items': items,
            'user': request.user,
            'is_show': True
        })
    else:
         return render_to_response('manage_housekeeping_item.html', {
             'user': request.user,
             'is_show': False
        })

@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def add_housekeeping_item(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        housekeeping_price_description = request.POST.get('housekeeping_price_description', None)
        housekeeping_item_name = request.POST.get('housekeeping_item_name', None)
        housekeeping_content = request.POST.get('housekeeping_content', None)
        housekeeping_remarks = request.POST.get('housekeeping_remarks', None)
        if housekeeping_price_description and housekeeping_item_name and housekeeping_content and housekeeping_remarks:
            item = Housekeeping_items()
            item.price_description = housekeeping_price_description
            item.item = housekeeping_item_name
            item.content = housekeeping_content
            item.remarks = housekeeping_remarks
            item.save()
            response_data = {'success': True}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def submit_housekeeping(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        housekeeping_array = request.POST.get("housekeeping_item_string", None)
        list_housekeeping = str(housekeeping_array).split(",")
        profile = ProfileDetail.objects.get(profile=request.user)
        for i in range(len(list_housekeeping)):
            hou_id = int(list_housekeeping[i])
            housekeeping_item = Housekeeping_items.objects.get(id=hou_id)
            housekeeping = Housekeeping()
            housekeeping.author = profile
            housekeeping.status = 1
            housekeeping.community = profile.community
            housekeeping.time = datetime.datetime.utcnow().replace(tzinfo=utc)
            housekeeping.housekeeping_item = housekeeping_item
            housekeeping.save()
        response_data = {'success': True, 'info': '提交成功！'}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def delete_housekeeping_item(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        housekeeping_array = request.POST.get("selected_item_string", None)
        if housekeeping_array:
            list_housekeeping_item = str(housekeeping_array).split(",")
            for i in range(len(list_housekeeping_item)):
                housekeeping_id = int(list_housekeeping_item[i])
                Housekeeping_items.objects.get(id=housekeeping_id).delete()
            response_data = {'success': True, 'info': '删除成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def deal_housekeeping(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        housekeeping_array = request.POST.get("selected_housekeeping_string", None)
        deal_person_id = request.POST.get("deal_person_id", None)
        if housekeeping_array and deal_person_id:
            list_housekeeping = str(housekeeping_array).split(",")
            for i in range(len(list_housekeeping)):
                house_id = int(list_housekeeping[i])
                housekeeping = Housekeeping.objects.get(id=house_id)
                housekeeping.status = 2
                user_obj = User.objects.get(id=deal_person_id)
                if user_obj:
                    housekeeping.handler = user_obj
                housekeeping.save()
            response_data = {'success': True, 'info': '授权成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")



@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def housekeeping_complete(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        housekeeping_array = request.POST.get("selected_housekeeping_string", None)
        if housekeeping_array :
            list_housekeeping= str(housekeeping_array).split(",")
            for i in range(len(list_housekeeping)):
                house_id = int(list_housekeeping[i])
                housekeeping = Housekeeping.objects.get(id=house_id)
                housekeeping.status = 3
                housekeeping.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")



@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def own_housekeeping(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    housekeepings = Housekeeping.objects.filter(author=profile)
    if len(housekeepings) > 0:
        paginator = Paginator(housekeepings, 5)
        page = request.GET.get('page')
        try:
            housekeeping_list = paginator.page(page)
        except PageNotAnInteger:
            housekeeping_list = paginator.page(1)
        except EmptyPage:
            housekeeping_list = paginator.page(paginator.num_pages)
        return render_to_response('own_housekeeping.html', {
                            'housekeeping_list': housekeeping_list,
                            'user': request.user,
                            'profile': profile,
                            'show': True
                        })
    return render_to_response('own_housekeeping.html',{ 'show': False ,'user':request.user,'profile':profile })



@transaction.atomic
@csrf_exempt
@login_required
def housekeeping_response(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        housekeeping_id = request.POST.get("housekeeping_id", None)
        response_content = request.POST.get("response_content", None)
        selected_pleased = request.POST.get("selected_radio", None)
        profile = ProfileDetail.objects.get(profile=request.user)
        housekeeping = Housekeeping.objects.get(id=housekeeping_id)
        if housekeeping:
            housekeeping.pleased_reason = response_content
            housekeeping.pleased = selected_pleased
            housekeeping.save()
            response_data = {'success': True, 'info': '评论成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            return render_to_response('own_housekeeping.html',{ 'show': True ,'user':request.user,'profile':profile })


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def modify_housekeeping_item(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        modify_item_id = request.POST.get('modify_item_id', None)
        housekeeping_price_description = request.POST.get('modify_price_description', None)
        housekeeping_item_name = request.POST.get('modify_item_name', None)
        housekeeping_content = request.POST.get('modify_content', None)
        housekeeping_remarks = request.POST.get('modify_remarks', None)
        item = Housekeeping_items.objects.get(id=modify_item_id)
        if housekeeping_price_description or housekeeping_item_name or housekeeping_content or housekeeping_remarks:
            if housekeeping_price_description:
                item.price_description = housekeeping_price_description
            if housekeeping_item_name:
                item.item = housekeeping_item_name
            if housekeeping_content:
                item.content = housekeeping_content
            if housekeeping_remarks:
                item.remarks = housekeeping_remarks
            item.save()
            response_data = {'success': True}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")

