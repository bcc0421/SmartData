#coding:utf-8
from django.db import transaction
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from SmartDataApp.models import Community
from SmartDataApp.views import index


@transaction.atomic
@csrf_exempt
def add_community(request):
    if request.method != u'POST':
        return render_to_response('add_community.html', {'user': request.user})
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

