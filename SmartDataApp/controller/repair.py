#coding:utf-8
import threading
from urllib import unquote

from django.http import HttpResponse
import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.utils.http import *

from SmartDataApp.controller.admin import convert_session_id_to_user
from SmartDataApp.controller.complain import UTC, push_message
from SmartDataApp.models import Repair
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail, Repair_item, Community, Wallet


def return_error_response():
    response_data = {'error': 'Just support POST method.'}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


def return_404_response():
    return HttpResponse('', content_type='application/json', status=404)

class ThreadClass(threading.Thread):
  def __init__(self, description, handler_detail, title):
      threading.Thread.__init__(self)
      self._description = description
      self._handler_detail = handler_detail
      self._title = title
  def run(self):
    #push_message(self._description, self._handler_detail, self._title)
    try:
        push_message(self._description, self._handler_detail, self._title)
    except Exception ,e:
        print e
        push_message(self._description, self._handler_detail, self._title)

@csrf_exempt
@login_required(login_url='/login/')
def repair(request):
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
    deal_person_list = ProfileDetail.objects.filter(is_admin=True,community=one_community)
    if request.user.is_staff:
        if deal_status == u'1':
            repairs = Repair.objects.filter(community=one_community, status=1).order_by('-timestamp')
            btn_status = 1
        elif deal_status == u'2':
            repairs = Repair.objects.filter(community=one_community, status=2).order_by('-timestamp')
            btn_status = 2
        elif deal_status == u'3':
            repairs = Repair.objects.filter(community=one_community, status=3).order_by('-timestamp')
            btn_status = 3
        elif deal_status == u'4':
            repairs = Repair.objects.filter(community=one_community, status=4).order_by('-timestamp')
            btn_status = 4
        else:
            repairs = Repair.objects.filter(community=one_community, status=1).order_by('-timestamp')
            btn_status = 1
        if len(repairs) > 0:
            paginator = Paginator(repairs, 4)
            page = request.GET.get('page')
            try:
                repairs_list = paginator.page(page)
            except PageNotAnInteger:
                repairs_list = paginator.page(1)
            except EmptyPage:
                repairs_list = paginator.page(paginator.num_pages)
            return render_to_response('admin_repair.html', {
                'repairs': repairs_list,
                'show': True,
                'btn_style': btn_status,
                'community': one_community,
                'change_community': status,
                'communities': communities,
                'profile': profile,
                'user': request.user,
                'deal_person_list': deal_person_list,
                'is_admin': False
            })
        else:
            return render_to_response('admin_repair.html', {
                'show': False,
                'user': request.user,
                'btn_style': btn_status,
                'community': one_community,
                'change_community': status,
                'communities': communities,
                'profile': profile,
                'deal_person_list': deal_person_list,
                'is_admin': False
            })

    elif profile.is_admin:
        if deal_status == u'2':
            repairs = Repair.objects.filter(handler=request.user, status=2).order_by('-timestamp')
            btn_status = 2
        elif deal_status == u'3':
            repairs = Repair.objects.filter(handler=request.user, status=3).order_by('-timestamp')
            btn_status = 3
        elif deal_status == u'4':
            repairs = Repair.objects.filter(handler=request.user, status=4).order_by('-timestamp')
            btn_status = 4
        else:
            repairs = Repair.objects.filter(handler=request.user, status=4).order_by('-timestamp')
            btn_status = 4
        if len(repairs) > 0:
            paginator = Paginator(repairs, 4)
            page = request.GET.get('page')
            try:
                repairs_list = paginator.page(page)
            except PageNotAnInteger:
                repairs_list = paginator.page(1)
            except EmptyPage:
                repairs_list = paginator.page(paginator.num_pages)
            return render_to_response('worker_repair.html', {
                'repairs': repairs_list,
                'show': True,
                'community': one_community,
                'btn_style': btn_status,
                'change_community': status,
                'communities': communities,
                'profile': profile,
                'user': request.user,
                'is_admin': True
            })
        else:
            return render_to_response('worker_repair.html', {
                'show': False,
                'btn_style': btn_status,
                'community': one_community,
                'change_community': status,
                'communities': communities,
                'profile': profile,
                'user': request.user,
                'is_admin': True
            })
    else:
        items = Repair_item.objects.all()
        item_person_list = list()
        item_public_list = list()
        for item in items:
            if item.type == u'个人报修':
                data = {
                    'item_id': item.id,
                    'item_type': item.type,
                    'item_price': item.price,
                    'item_name': item.item,
                }
                item_person_list.append(data)
            else:
                data = {
                    'item_id': item.id,
                    'item_type': item.type,
                    'item_price': item.price,
                    'item_name': item.item,
                }
                item_public_list.append(data)
        return render_to_response('repair.html', {'user': request.user,
                                                  'item_person_list': item_person_list,
                                                  'item_public_list': item_public_list,
                                                  'community': one_community,
                                                  'change_community': status,
                                                  'communities': communities,
                                                  'profile': profile
        })


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def repair_create(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        category_id = None
        communities = Community.objects.all()
        repair_content = request.POST.get('content', None)
        repair_type = request.POST.get('category', None)
        category_person_id = request.POST.get('category_person', None)
        category_public_id = request.POST.get('category_public', None)
        upload_repair_src = request.FILES.get('upload_repair_img', None)
        profile = ProfileDetail.objects.get(profile=request.user)
        repair_time = datetime.datetime.now()
        if repair_type == u'个人报修':
            category_id = category_person_id
            repair_type = 1
        else:
            category_id = category_public_id
            repair_type = 0
        if category_id:
            item = Repair_item.objects.get(id=category_id)
            if repair_content or repair_type:
                repair = Repair()
                repair.content = repair_content
                repair.timestamp = repair_time
                repair.status = 1
                repair.author_detail = profile
                repair.author = request.user.username
                repair.type = repair_type
                repair.repair_item = item.item
                repair.price = item.price
                repair.community = profile.community
                repair.is_admin_read = True
                if upload_repair_src:
                    repair.src = upload_repair_src
                repair.save()
                return render_to_response('repair_success.html',
                                          {'user': request.user, 'communities': communities, 'profile': profile,
                                           'change_community': 2})
            else:
                return render_to_response('repair.html',
                                          {'user': request.user, 'communities': communities, 'profile': profile,
                                           'change_community': 2})
        else:
                return render_to_response('repair.html',
                                          {'user': request.user, 'communities': communities, 'profile': profile,
                                           'change_community': 2,})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def repair_deal(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_array = request.POST.get("selected_repair_string", None)
        deal_person_id = request.POST.get("deal_person_id", None)
        if repair_array and deal_person_id:
            deal_person=User.objects.get(id=deal_person_id)
            handler_detail = ProfileDetail.objects.get(profile=deal_person)
            if handler_detail.device_user_id and handler_detail.device_chanel_id and handler_detail.device_type:
                list_repair = str(repair_array).split(",")
                for i in range(len(list_repair)):
                    re_id = int(list_repair[i])
                    repair = Repair.objects.get(id=re_id)
                    repair.is_read = True
                    repair.is_worker_read = True
                    repair.status = 4
                    user_obj = deal_person
                    if user_obj:
                        repair.handler = user_obj
                    repair.save()
                title = '消息通知'
                description = '你有新的报修需要处理请查看！'
                push_class = ThreadClass(description, handler_detail, title)
                push_class.start()
                #push_message(description, handler_detail, title)
                response_data = {'success': True, 'info': '授权成功并推送消息至处理人！'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
            else:
                response_data = {'success': False, 'info': '请工作人员绑定手机端'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")

@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def worker_deal_repair(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_array = request.POST.get("selected_repair_string", None)
        if repair_array:
            list_repair = str(repair_array).split(",")
            for i in range(len(list_repair)):
                re_id = int(list_repair[i])
                repair = Repair.objects.get(id=re_id)
                repair.is_read = True
                repair.is_worker_read = True
                repair.status = 2
                user_obj = User.objects.get(username=repair.author)
                repair.save()
                profile = ProfileDetail.objects.get(profile=user_obj)
                title = '消息通知'
                description = '你的报修已经授权处理！'
                if profile.device_user_id and profile.device_chanel_id and profile.device_type:
                    try:
                        push_class = ThreadClass(description, profile, title)
                        push_class.start()
                        #push_message(description, profile, title)
                    except Exception,e:
                        #print e
                        continue
            response_data = {'success': True, 'info': '工作人员处理中'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")

@transaction.atomic
@csrf_exempt
@login_required
def complete_repair(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_array = request.POST.get("selected_repair_string", None)
        if repair_array:
            list_repair = str(repair_array).split(",")
            for i in range(len(list_repair)):
                com_id = int(list_repair[i])
                repair = Repair.objects.get(id=com_id)
                repair.complete_time = datetime.datetime.now()
                repair.status = 3
                repair.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required
def own_repair(request):
    start_time = request.POST.get('start_time', None)
    end_time = request.POST.get('end_time', None)
    if start_time and end_time:
        repairs = Repair.objects.filter(author=request.user.username, timestamp__range=[start_time, end_time])
    else:
        repairs = Repair.objects.filter(author=request.user.username).order_by('-timestamp')
    profile = ProfileDetail.objects.get(profile=request.user)
    wallet = Wallet.objects.filter(user_profile=profile)
    if wallet:
        wallet = wallet[0]
    communities = Community.objects.all()
    if len(repairs) > 0:
        paginator = Paginator(repairs, 7)
        page = request.GET.get('page')
        try:
            repairs_list = paginator.page(page)
        except PageNotAnInteger:
            repairs_list = paginator.page(1)
        except EmptyPage:
            repairs_list = paginator.page(paginator.num_pages)
        return render_to_response('own_repair.html', {
            'repairs': repairs_list,
            'user': request.user,
            'wallet': wallet,
            'profile': profile,
            'show': True
        })
    return render_to_response('own_repair.html',
                              {'show': False, 'user': request.user, 'communities': communities, 'profile': profile,
                               'change_community': 2, 'wallet': wallet,})


@transaction.atomic
@csrf_exempt
@login_required
def repair_response(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_id = request.POST.get("repair_id", None)
        response_content = request.POST.get("response_content", None)
        selected_pleased = request.POST.get("selected_radio", None)
        profile = ProfileDetail.objects.get(profile=request.user)
        repair = Repair.objects.get(id=repair_id)
        handler_profile = ProfileDetail.objects.get(profile=repair.handler)
        title = '消息通知'
        description = '用户已对你的处理作出评价！'
        if repair:
            repair.pleased_reason = response_content
            repair.pleased = selected_pleased
            repair.save()
            push_class = ThreadClass(description, handler_profile, title)
            push_class.start()
            response_data = {'success': True, 'info': '评论成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            return render_to_response('own_repair.html', {'show': True, 'user': request.user, 'profile': profile})

@transaction.atomic
@csrf_exempt
def repair_delete(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_array = request.POST.get("selected_repair_string", None)
        if repair_array:
            list_repair = str(repair_array).split(",")
            for i in range(len(list_repair)):
                com_id = int(list_repair[i])
                Repair.objects.get(id=com_id).delete()
            response_data = {'success': True, 'info': '删除成功'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")

@transaction.atomic
@csrf_exempt
def api_repair_create(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    else:
        repair_content = request.POST.get('content', None)
        repair_type = request.POST.get('category', None)
        category_item_id = request.POST.get('category_item_id', None)
        upload_repair_src = request.FILES.get('upload_repair_img', None)
        repair_time = datetime.datetime.now()
        item = Repair_item.objects.get(id=category_item_id)
        profile = ProfileDetail.objects.get(profile=request.user)
        if repair_type:
            repair = Repair()
            repair.content = repair_content
            repair.timestamp = repair_time
            repair.status = 1
            repair.author = request.user.username
            repair.author_detail = profile
            repair.type = repair_type
            repair.repair_item = item.item
            repair.price = item.price
            repair.community = profile.community
            repair.is_read = True
            if upload_repair_src:
                repair.src = upload_repair_src
            repair.save()
            return HttpResponse(simplejson.dumps({'error': False, 'info': u'报修创建成功'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'error': True, 'info': u'报修创建失败'}),
                                content_type='application/json')


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def api_worker_deal_repair(request):
    if request.method != u'POST':
        return redirect(index)
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        repair_array = data.get("repair_id_string", None)
        if repair_array:
            list_repair = str(repair_array).split(",")
            for i in range(len(list_repair)):
                re_id = int(list_repair[i])
                repair = Repair.objects.get(id=re_id)
                repair.is_read = True
                repair.is_worker_read = True
                repair.status = 2
                user_obj = User.objects.get(username=repair.author)
                repair.save()
                profile = ProfileDetail.objects.get(profile=user_obj)
                title = '消息通知'
                description = '你的报修已经授权处理！'
                if profile.device_user_id and profile.device_chanel_id and profile.device_type:
                    try:
                        push_class = ThreadClass(description, profile, title)
                        push_class.start()
                        #push_message(description, profile, title)
                    except Exception,e:
                        #print e
                        continue
            response_data = {'success': True, 'info': '已更改状态并发送消息至客户！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
    else:
        response_data = {'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_repair_response(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        repair_id = data.get("repair_id", None)
        response_content = data.get("response_content", None)
        selected_pleased = data.get("selected_pleased", None)
        repair = Repair.objects.get(id=repair_id)
        handler_profile = ProfileDetail.objects.get(profile=repair.handler)
        title = '消息通知'
        description = '用户已对你的处理作出评价！'
        if repair and selected_pleased:
            repair.pleased_reason = response_content
            repair.pleased = selected_pleased
            repair.save()
            push_class = ThreadClass(description, handler_profile, title)
            push_class.start()
            response_data = {'success': True, 'info': '反馈成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
        else:
            response_data = {'success': False, 'info': '反馈失败！'}
            return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        return return_404_response()


@transaction.atomic
@csrf_exempt
def api_own_repair(request):
    convert_session_id_to_user(request)
    repairs = Repair.objects.filter(author=request.user.username).order_by('-timestamp')
    if len(repairs) > 0:
        paginator = Paginator(repairs, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            repairs_list = paginator.page(page).object_list
        except PageNotAnInteger:
            repairs_list = paginator.page(1)
        except EmptyPage:
            repairs_list = paginator.page(paginator.num_pages)
        repair_list = list()
        for repair_detail in repairs_list:
            time = repair_detail.timestamp
            local = time.astimezone(UTC(8))
            data = {
                'id': repair_detail.id,
                'repair_author': repair_detail.author,
                'author_community': repair_detail.community.title,
                'author_floor': repair_detail.author_detail.floor,
                'author_room': repair_detail.author_detail.gate_card,
                'content': repair_detail.content,
                'type': repair_detail.type,
                'deal_status': repair_detail.status,
                'pleased': repair_detail.pleased,
                'src': repair_detail.src.name,
                'time': str(local).split('.')[0],
                'handler': str(repair_detail.handler)
            }
            repair_list.append(data)
        response_data = {'repair_list': repair_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_repair_deal(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        repair_array = data.get("repair_id_string", None)
        deal_person_id = data.get("deal_person_id", None)
        deal_person = User.objects.get(id=deal_person_id)
        handler_detail = ProfileDetail.objects.get(profile=deal_person)
        if handler_detail.device_user_id and handler_detail.device_chanel_id and handler_detail.device_type:
            if repair_array and deal_person_id:
                list_repair = str(repair_array).split(",")
                for i in range(len(list_repair)):
                    rep_id = int(list_repair[i])
                    repair = Repair.objects.get(id=rep_id)
                    repair.status = 4
                    repair.is_read = True
                    repair.is_worker_read = True
                    user_obj = deal_person
                    if user_obj:
                        repair.handler = user_obj
                    repair.save()
                title = '消息通知'
                description = '你有新的报修需要处理请查看！'
                push_class = ThreadClass(description, handler_detail, title)
                push_class.start()
                #push_message(description, handler_detail, title)
                response_data = {'success': True, 'info': '授权成功并推送消息至处理人！'}
                return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '请工作人员帮定手机端'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_repair_complete(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        repair_array = data.get("repair_id_string", None)
        if repair_array:
            list_repair = str(repair_array).split(",")
            for i in range(len(list_repair)):
                rep_id = int(list_repair[i])
                repair = Repair.objects.get(id=rep_id)
                repair.complete_time = datetime.datetime.now()
                repair.status = 3
                repair.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_show_all_repair(request):
    convert_session_id_to_user(request)

    community_id = request.GET.get("community_id", None)
    if community_id:
        community = Community.objects.get(id=community_id)
    else:
        response_data = {'info': '没有传入小区id', 'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    repairs = Repair.objects.filter(community=community).order_by('-timestamp')
    if len(repairs) > 0:
        paginator = Paginator(repairs, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            repairs_list = paginator.page(page).object_list
        except PageNotAnInteger:
            repairs_list = paginator.page(1)
        except EmptyPage:
            repairs_list = paginator.page(paginator.num_pages)
        repair_list = list()
        for repair_detail in repairs_list:
            time = repair_detail.timestamp
            local = time.astimezone(UTC(8))
            data = {
                'id': repair_detail.id,
                'repair_author': repair_detail.author,
                'author_community': repair_detail.community.title,
                'author_floor': repair_detail.author_detail.floor,
                'author_room': repair_detail.author_detail.gate_card,
                'content': repair_detail.content,
                'type': repair_detail.type,
                'deal_status': repair_detail.status,
                'pleased': repair_detail.pleased,
                'src': repair_detail.src.name,
                'time': str(local).split('.')[0],
                'handler': str(repair_detail.handler)
            }
            repair_list.append(data)
        response_data = {'repair_list': repair_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_show_repair_by_status(request):
    convert_session_id_to_user(request)
    community_id = request.GET.get("community_id", None)
    repair_status = request.GET.get("status", None)
    profile = ProfileDetail.objects.get(profile=request.user)
    if community_id:
        community = Community.objects.get(id=community_id)
    else:
        response_data = {'info': '没有传入小区id', 'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    if request.user.is_staff:
        repairs = Repair.objects.filter(community=community, status=int(str(repair_status))).order_by('-timestamp')
    elif profile.is_admin:
        repairs = Repair.objects.filter(community=community, status=int(str(repair_status)), handler=request.user).order_by('-timestamp')
    else:
        repairs = Repair.objects.filter(community=community, status=int(str(repair_status)), author=request.user.username).order_by('-timestamp')

    if len(repairs) > 0:
        paginator = Paginator(repairs, 20)
        page_count = paginator.num_pages
        page = request.GET.get('page')
        try:
            repairs_list = paginator.page(page).object_list
        except PageNotAnInteger:
            repairs_list = paginator.page(1)
        except EmptyPage:
            repairs_list = paginator.page(paginator.num_pages)
        repair_list = list()
        for repair_detail in repairs_list:
            time = repair_detail.timestamp
            local = time.astimezone(UTC(8))
            data = {
                'id': repair_detail.id,
                'repair_author': repair_detail.author,
                'author_community': repair_detail.community.title,
                'author_floor': repair_detail.author_detail.floor,
                'author_room': repair_detail.author_detail.gate_card,
                'content': repair_detail.content,
                'type': repair_detail.type,
                'deal_status': repair_detail.status,
                'pleased': repair_detail.pleased,
                'src': repair_detail.src.name,
                'time': str(local).split('.')[0],
                'handler': str(repair_detail.handler)
            }
            repair_list.append(data)
        response_data = {'repair_list': repair_list, 'page_count': page_count, 'success': True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_repair_create_android(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    else:
        repair_content = unquote(str(request.POST.get('content', None)))
        repair_type = unquote(str(request.POST.get('category', None)))
        category_item_id = request.POST.get('category_item_id', None)
        #upload_repair_src = unquote(str(request.FILES.get('upload_repair_img', None)))
        upload_repair_src = request.FILES.get('upload_repair_img', None)
        repair_time = datetime.datetime.now()
        item = Repair_item.objects.get(id=category_item_id)
        profile = ProfileDetail.objects.get(profile=request.user)
        if repair_type:
            repair = Repair()
            repair.content = repair_content
            repair.timestamp = repair_time
            repair.status = 1
            repair.author = request.user.username
            repair.author_detail = profile
            repair.type = repair_type
            repair.repair_item = item.item
            repair.price = item.price
            repair.community = profile.community
            repair.is_read = True
            if upload_repair_src:
                repair.src = upload_repair_src
            repair.save()
            return HttpResponse(simplejson.dumps({'error': False, 'info': u'报修创建成功'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'error': True, 'info': u'报修创建失败'}),
                                content_type='application/json')