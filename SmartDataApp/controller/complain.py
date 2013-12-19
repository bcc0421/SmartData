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
from SmartDataApp.models import Complaints ,Repair
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail

def return_error_response():
    response_data = {'error': 'Just support POST method.'}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')

def return_404_response():
    return HttpResponse('', content_type='application/json', status=404)

@csrf_exempt
@login_required(login_url='/login/')
def complain(request):
        profile = ProfileDetail.objects.get(profile=request.user)
        if request.user.is_staff:
            complains = Complaints.objects.all().order_by('-timestamp')
            deal_person_list = ProfileDetail.objects.filter(is_admin=True)
            if len(complains) > 0:
                return render_to_response('admin_complains.html', {
                    'complains': list(complains),
                    'show': True,
                    'user': request.user,
                    'deal_person_list': deal_person_list,
                    'is_admin': False
                })
            else:
                return render_to_response('admin_complains.html', {
                    'show': False,
                    'user': request.user,
                    'deal_person_list': deal_person_list,
                    'is_admin': False
                })
        elif profile.is_admin:
            complains = Complaints.objects.filter(handler = request.user).order_by('-timestamp')
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
def complain_create(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_content = request.POST.get('content', None)
        complain_type = request.POST.get('category', None)
        upload__complain_src = request.FILES.get('upload_complain_img', None)
        complain_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        if complain_content or complain_type:
            complain = Complaints()
            complain.content = complain_content
            complain.timestamp = complain_time
            complain.status = 1
            complain.author = request.user.username
            complain.type = complain_type
            if upload__complain_src:
                complain.src = upload__complain_src
            complain.save()
            return render_to_response('complain_sucess.html', {'user': request.user})
        else:
            return render_to_response('complains.html', {'user': request.user})


@transaction.atomic
@csrf_exempt
def complain_deal(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_array = request.POST.get("selected_complain_string", None)
        deal_person_id = request.POST.get("deal_person_id", None)
        if complain_array and deal_person_id:
            list_complain_ = str(complain_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                complain = Complaints.objects.get(id=com_id)
                complain.status = 2
                user_obj = User.objects.get(id=deal_person_id)
                if user_obj:
                    complain.handler = user_obj
                complain.save()
            response_data = {'success': True, 'info': '授权成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def complain_complete(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_array = request.POST.get("selected_complain_string", None)
        if complain_array :
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
    complains = Complaints.objects.filter(author=request.user.username)
    profile = ProfileDetail.objects.get(profile=request.user)
    if len(complains) > 0:
        paginator = Paginator(complains, 5)
        page = request.GET.get('page')
        try:
            complains_list = paginator.page(page)
        except PageNotAnInteger:
            complains_list = paginator.page(1)
        except EmptyPage:
            complains_list = paginator.page(paginator.num_pages)
        return render_to_response('own_complain.html', {
                        'complains':complains_list,
                        'user':request.user,
                        'profile':profile ,
                        'show': True
                    })
    return render_to_response('own_complain.html',{ 'show': False ,'user':request.user,'profile':profile })


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
            complain.pleased_reason=response_content
            complain.pleased=selected_pleased
            complain.save()
            response_data = {'success': True, 'info': '评论成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            return render_to_response('own_complain.html',{ 'show': True ,'user':request.user,'profile':profile })




@csrf_exempt
def show_image_detail(request,id):
    if request.method != u'GET':
        return redirect(index)
    else:
        type = request.GET.get("type",None)
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
        complain_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        if complain_content or complain_type:
            complain = Complaints(author=request.user.username)
            complain.content = complain_content
            complain.timestamp = complain_time
            complain.type = complain_type
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
        paginator = Paginator(complains, 5)
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
                data = {
                    'id': complain_detail.id,
                    'complain_author': complain_detail.author,
                    'content': complain_detail.content,
                    'type': complain_detail.type,
                    'deal_status': complain_detail.status,
                    'pleased': complain_detail.pleased,
                    'src': complain_detail.src.name,
                    'time': str(complain_detail.timestamp)
                }
                complain_list.append(data)
        response_data = {'complain_list': complain_list, 'page_count': page_count}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_complain_deal(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        complain_array = data .get("complains_id_string", None)
        deal_person_id = data .get("deal_person_id", None)
        if complain_array and deal_person_id:
            list_complain_ = str(complain_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                complain = Complaints.objects.get(id=com_id)
                complain.status = 2
                user_obj = User.objects.get(id=deal_person_id)
                if user_obj:
                    complain.handler = user_obj
                complain.save()
            response_data = {'success': True, 'info': u'授权成功！'}
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
        complain_array = data .get("complains_id_string", None)
        if complain_array :
            list_complain_ = str(complain_array).split(",")
            for i in range(len(list_complain_)):
                com_id = int(list_complain_[i])
                complain = Complaints.objects.get(id=com_id)
                complain.status = 3
                complain.save()
            response_data = {'success': True, 'info': '提交成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")