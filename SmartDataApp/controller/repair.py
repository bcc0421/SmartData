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
from SmartDataApp.models import Repair
from SmartDataApp.views import index
from SmartDataApp.models import ProfileDetail

@csrf_exempt
@login_required(login_url='/login/')
def repair(request):
    if not request.user.is_staff:
            return render_to_response('repair.html', {'user': request.user})
    else:
            repairs = Repair.objects.all()
            deal_person_list = ProfileDetail.objects.filter(is_admin=True)
            if len(repairs) > 0:
                return render_to_response('admin_repair.html', {
                    'repairs': list(repairs),
                    'show': True,
                    'user': request.user,
                    'deal_person_list':deal_person_list
                })
            else:
                return render_to_response('admin_repair.html', {
                    'show': False,
                    'user': request.user,
                    'deal_person_list':deal_person_list
                })


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def  repair_create(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        repair_content = request.POST.get('content', None)
        repair_type = request.POST.get('category', None)
        upload_repair_src = request.FILES.get('upload_repair_img', None)
        repair_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        if repair_content or repair_type:
            repair = Repair(author=request.user)
            repair.content = repair_content
            repair.timestamp = repair_time
            repair.type =repair_type
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
            list_repair= str(repair_array).split(",")
            for i in range(len(list_repair)):
                re_id = int(list_repair[i])
                repair = Repair.objects.get(id=re_id)
                repair.status = True
                user_obj = User.objects.get(id=deal_person_id)
                if user_obj:
                    profile = ProfileDetail.objects.get(profile=user_obj)
                    repair.handler.add(profile)
                repair.save()
            response_data = {'success': True, 'info': '授权成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def own_repair(request):
    repairs=Repair.objects.filter(author=request.user)
    profile=ProfileDetail.objects.get(profile=request.user)
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
                        'repairs':repairs_list,
                        'user':request.user,
                        'profile':profile ,
                        'show': True
                    })
    return render_to_response('own_repair.html',{ 'show': False ,'user':request.user,'profile':profile })