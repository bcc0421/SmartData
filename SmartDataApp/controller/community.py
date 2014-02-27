#coding:utf-8
import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
import simplejson
from SmartDataApp.controller.admin import convert_session_id_to_user, return_error_response
from SmartDataApp.models import Community, ProfileDetail, Notification
from SmartDataApp.views import index


@transaction.atomic
@csrf_exempt
@login_required
def add_community(request):
    if request.method != u'POST':
        communities = Community.objects.all()
        return render_to_response('add_community.html', {'user': request.user, 'communities':communities})
    else:
        name = request.POST.get(u'name', None)
        description = request.POST.get(u'description', None)
        communities = Community.objects.filter(title=name)
        if len(communities) > 0:
            return render_to_response('add_community.html', {
                'user': request.user,
                'name_error': True,
                'info': '该社区名称已经存在'
            })
        else:
            community = Community(title=name)
            community.description = description
            community.save()
            return redirect(index)


def update_community(request):
    pass


def delete_community(request):
    pass

@csrf_exempt
def enter_community(request, id):
    community = Community.objects.get(id=id)
    communities = Community.objects.all()
    request.session['community_id'] = id
    request.session.set_expiry(3600*24*7)
    if request.user.is_authenticated():
        return render_to_response('index.html', {
                        'community': community,
                        'communities': communities,
                        'change_community': 1,
                        'user': request.user,
                    })
    else:
        return render_to_response('index.html', {'communities': communities,'change_community': 1, 'community': community})

@transaction.atomic
@csrf_exempt
def api_get_community(request):
    convert_session_id_to_user(request)
    communities = Community.objects.all()
    if communities:
        community_list = list()
        for community_detail in communities:
                    data = {
                        'id': community_detail.id,
                        'community_title': community_detail.title,
                        'community_description':community_detail.description
                    }
                    community_list.append(data)
        response_data = {'community_list': community_list, 'success':True}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')
    else:
        response_data = {'success': False}
        return HttpResponse(simplejson.dumps(response_data), content_type='application/json')



@transaction.atomic
@csrf_exempt
def add_notification(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community = Community.objects.get(id=profile.community.id)
    notification_title = request.POST.get('notification_title', None)
    #notification_time = request.POST.get('notification_time', None)
    notification_content = request.POST.get('notification_content', None)
    notification = Notification()
    notification.notification_community = community
    notification.notification_content = notification_content
    notification.notification_theme = notification_title
    notification.notification_time = datetime.datetime.now()
    notification.save()
    response_data = {'info': '添加成功', 'success': True}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')

@transaction.atomic
@csrf_exempt
def modify_notification(request):
    modify_id = request.POST.get('modify_id', None)
    modify_title = request.POST.get('modify_title', None)
    modify_content = request.POST.get('modify_content', None)
    notification = Notification.objects.get(id=modify_id)
    notification.notification_content = modify_content
    notification.notification_theme = modify_title
    notification.save()
    response_data = {'info': '修改成功', 'success': True}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')


@transaction.atomic
@csrf_exempt
def delete_notification(request):
    delete_id = request.POST.get('delete_id', None)
    Notification.objects.get(id=delete_id).delete()
    response_data = {'info': '删除成功', 'success': True}
    return HttpResponse(simplejson.dumps(response_data), content_type='application/json')



@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def community_notification(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    community = Community.objects.get(id=profile.community.id)
    notification = Notification.objects.filter(notification_community=community)
    #notification = community.
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    if request.user.is_staff:
        return render_to_response('admin_community_notification.html',
                                  {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status,'notifications':notification})

    else:
      return render_to_response('user_community_notification.html', {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status})


@transaction.atomic
@csrf_exempt
@login_required(login_url='/login/')
def notification_detail(request):
    profile = ProfileDetail.objects.get(profile=request.user)
    community_id = request.session.get('community_id', profile.community.id)
    one_community = Community.objects.get(id=community_id)
    notification_id = request.GET.get('id', None)
    notification = Notification.objects.get(id=notification_id)
    status = None
    if community_id == profile.community.id:
        status = 2
    else:
        status = 1
    communities = Community.objects.all()
    return render_to_response('notification_detail.html',
        {'user': request.user,'profile': profile,'communities': communities,'community': one_community, 'change_community': status,'notification':notification})

