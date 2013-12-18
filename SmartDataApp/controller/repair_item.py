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
from SmartDataApp.models import ProfileDetail,Repair_item


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def repair_item(request):
    items = Repair_item.objects.all()
    if len(items) > 0:
        return render_to_response('manage_repair_item.html', {
            'items':items,
            'is_show':True
        })
    else:
         return render_to_response('manage_repair_item.html', {
            'is_show':False
        })



@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def add_repair_item(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        item_type = request.POST.get('item_type', None)
        item_name = request.POST.get('item_name', None)
        repair_item_price = request.POST.get('repair_item_price', None)
        if item_type and item_name and repair_item_price:
            item = Repair_item()
            item.price = repair_item_price
            item.item = item_name
            item.type = item_type
            item.save()
            response_data = {'success': True}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def delete_repair_item(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        item_array = request.POST.get("selected_item_string", None)
        if item_array:
            list_item = str(item_array).split(",")
            for i in range(len(list_item)):
                item_id = int(list_item[i])
                Repair_item.objects.get(id=item_id).delete()
            response_data = {'success': True, 'info': '删除成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
