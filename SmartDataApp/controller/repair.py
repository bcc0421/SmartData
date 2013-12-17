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
from SmartDataApp.controller.admin import convert_session_id_to_user
from SmartDataApp.models import Repair
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail


def return_error_response():
    response_data = {'error': 'Just support POST method.'}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


def return_404_response():
    return HttpResponse('', content_type='application/json', status=404)


@csrf_exempt
@login_required(login_url='/login/')
def repair(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    if request.user.is_staff:
        repairs = Repair.objects.all().order_by('-timestamp')
        deal_person_list = ProfileDetail.objects.filter(is_admin=True)

        if len(repairs) > 0:
            return render_to_response('admin_repair.html', {
                'repairs': list(repairs),
                'show': True,
                'user': request.user,
                'deal_person_list': deal_person_list,
                'is_admin': False
            })
        else:
            return render_to_response('admin_repair.html', {
                'show': False,
                'user': request.user,
                'deal_person_list': deal_person_list,
                'is_admin': False
            })

    elif profile.is_admin:
        repairs = Repair.objects.filter(handler=request.user).order_by('-timestamp')
        if len(repairs) > 0:
            return render_to_response('admin_repair.html', {
                'repairs': list(repairs),
                'show': True,
                'user': request.user,
                'is_admin': True
            })
        else:
            return render_to_response('admin_repair.html', {
                'show': False,
                'user': request.user,
                'is_admin': True
            })
    else:
        return render_to_response('repair.html', {'user': request.user})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def repair_create(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_content = request.POST.get('content', None)
        repair_type = request.POST.get('category', None)
        upload_repair_src = request.FILES.get('upload_repair_img', None)
        repair_time = datetime.datetime.now()
        if repair_content or repair_type:
            repair = Repair()
            repair.content = repair_content
            repair.timestamp = repair_time
            repair.status = 1
            repair.author=request.user.username
            repair.type = repair_type
            if upload_repair_src:
                repair.src = upload_repair_src
            repair.save()
            return render_to_response('complain_sucess.html', {'user': request.user})
        else:
            return render_to_response('repair.html', {'user': request.user})


@transaction.atomic
@csrf_exempt
def repair_deal(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_array = request.POST.get("selected_repair_string", None)
        deal_person_id = request.POST.get("deal_person_id", None)
        if repair_array and deal_person_id:
            list_repair = str(repair_array).split(",")
            for i in range(len(list_repair)):
                re_id = int(list_repair[i])
                repair = Repair.objects.get(id=re_id)
                repair.status = 2
                user_obj = User.objects.get(id=deal_person_id)
                if user_obj:
                    repair.handler = user_obj
                repair.save()
            response_data = {'success': True, 'info': '授权成功！'}
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
                repair.status = 3
                repair.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required
def own_repair(request):
    repairs = Repair.objects.filter(author=request.user.username)
    profile = ProfileDetail.objects.get(profile=request.user)
    if len(repairs) > 0:
        paginator = Paginator(repairs, 5)
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
            'profile': profile,
            'show': True
        })
    return render_to_response('own_repair.html', {'show': False, 'user': request.user, 'profile': profile})


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
        if repair:
            repair.pleased_reason = response_content
            repair.pleased = selected_pleased
            repair.save()
            response_data = {'success': True, 'info': '评论成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            return render_to_response('own_repair.html', {'show': True, 'user': request.user, 'profile': profile})


@transaction.atomic
@csrf_exempt
def api_repair_create(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    else:
        repair_content = request.POST.get('content', None)
        repair_type = request.POST.get('category', None)
        upload__repair_src = request.FILES.get('upload_repair_img', None)
        repair_time = datetime.datetime.now()
        if repair_content or repair_type:
            repair = Repair(author=request.user.username)
            repair.content = repair_content
            repair.timestamp = repair_time
            repair.type = repair_type
            if upload__repair_src:
                repair.src = upload__repair_src
            repair.save()
            return HttpResponse(simplejson.dumps({'error': False, 'info': u'报修创建成功'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'error': True, 'info': u'报修创建失败'}),
                                content_type='application/json')


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
        if repair and selected_pleased:
            repair.pleased_reason = response_content
            repair.pleased = selected_pleased
            repair.save()
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
    repairs = Repair.objects.filter(author=request.user.username)
    if len(repairs) > 0:
        paginator = Paginator(repairs, 5)
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
            data = {
                'id': repair_detail.id,
                'repair_author': repair_detail.author,
                'content': repair_detail.content,
                'type': repair_detail.type,
                'deal_status': repair_detail.status,
                'pleased': repair_detail.pleased,
                'src': repair_detail.src.name,
                'time': str(repair_detail.timestamp)
            }
            repair_list.append(data)
        response_data = {'repair_list': repair_list, 'page_count': page_count}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')