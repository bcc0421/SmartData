#coding:utf-8
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
import simplejson
from SmartDataApp.controller.admin import convert_session_id_to_user, return_error_response
from SmartDataApp.models import Community
from SmartDataApp.views import index


@transaction.atomic
@csrf_exempt
# @login_required
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