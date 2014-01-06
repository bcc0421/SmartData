#coding:utf-8
from django.http import HttpResponse
import simplejson
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from SmartDataApp.controller.admin import convert_session_id_to_user, return_error_response
from SmartDataApp.views import index
from SmartDataApp.models import Repair_item


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def repair_item(request):
    items = Repair_item.objects.all()
    if len(items) > 0:
        return render_to_response('manage_repair_item.html', {
            'items': items,
            'user': request.user,
            'is_show': True
        })
    else:
        return render_to_response('manage_repair_item.html', {
            'user': request.user,
            'is_show': False
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


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def modify_repair_item(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        modify_item_id = request.POST.get('modify_item_id', None)
        item_type = request.POST.get('item_type', None)
        item_name = request.POST.get('item_name', None)
        repair_item_price = request.POST.get('repair_item_price', None)
        item = Repair_item.objects.get(id=modify_item_id)
        if item_type or item_name or repair_item_price:
            if repair_item_price:
                item.price = repair_item_price
            if item_name:
                item.item = item_name
            if item_type:
                item.type = item_type
            item.save()
            response_data = {'success': True}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
def api_get_repair_item(request):
    convert_session_id_to_user(request)
    item_type = request.GET.get("type", None)
    if item_type == u'个人':
        items = Repair_item.objects.filter(type='个人报修')
    if item_type == u'公共':
        items = Repair_item.objects.filter(type='公共报修')
    else:
        items = Repair_item.objects.all()
    if items:
        #paginator = Paginator(items, 5)
        #page_count = paginator.num_pages
        #page = request.GET.get('page')
        #try:
        #    items = paginator.page(page).object_list
        #except PageNotAnInteger:
        #    items = paginator.page(1)
        #except EmptyPage:
        #    items = paginator.page(paginator.num_pages)
        items_list = list()
        for item_detail in items:
            data = {
                'item_id': item_detail.id,
                'item_type': item_detail.type,
                'item_name': item_detail.item,
                'item_price': item_detail.price,
            }
            items_list.append(data)
        response_data = {'success': True, 'items_list': items_list}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False, 'info': '没有报修项目'}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def api_add_repair_item_record(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        item_type = data.get('item_type', None)
        item_name = data.get('item_name', None)
        repair_item_price = data.get('repair_item_price', None)
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
def api_repair_item_delete(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        item_array = data.get("repair_item_id_string", None)
        if item_array:
            list_item = str(item_array).split(",")
            for i in range(len(list_item)):
                item_id = int(list_item[i])
                Repair_item.objects.get(id=item_id).delete()
            response_data = {'success': True, 'info': '删除成功！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '删除失败！'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def api_modify_repair_item(request):
    if request.method != u'POST':
        return redirect(index)
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        modify_item_id = data.get('modify_item_id', None)
        item_type = data.get('item_type', None)
        item_name = data.get('item_name', None)
        repair_item_price = data.get('repair_item_price', None)
        item = Repair_item.objects.get(id=modify_item_id)
        if item_type or item_name or repair_item_price:
            if repair_item_price:
                item.price = repair_item_price
            if item_name:
                item.item = item_name
            if item_type:
                item.type = item_type
            item.save()
            response_data = {'success': True}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
        else:
            response_data = {'success': False, 'info': '没有修改信息'}
            return HttpResponse(simplejson.dumps(response_data), content_type="application/json")
