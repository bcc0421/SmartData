#coding:utf-8
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from SmartDataApp.models import Complaints
from SmartDataApp.views import index


@login_required()
def complain(request):
    if not request.user.is_staff:
        return render_to_response('complains.html', {'user': request.user})
    else:
        complains = Complaints.objects.all()
        if len(complains) > 0:
            paginator = Paginator(complains, 2)
            page = request.GET.get('page')
            try:
                complains_list = paginator.page(page)
            except PageNotAnInteger:
                complains_list = paginator.page(1)
            except EmptyPage:
                complains_list = paginator.page(paginator.num_pages)
            return render_to_response('admin_complains.html', {
                'complains': complains_list,
                'show': True,
                'user': request.user
            })
        else:
            return render_to_response('admin_complains.html', {
                'show': False,
                'user': request.user
            })


@transaction.atomic
@csrf_exempt
def complain_create(request):
    if request.method != u'POST':
        return redirect(index)
    else:
        complain_content = request.POST.get('content', None)
        complain_type = request.POST.get('category', None)
        upload__complain_src = request.FILES.get('upload_complain_img', None)
        complain_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        if complain_content or complain_type:
            complain = Complaints(author=request.user)
            complain.content = complain_content
            complain.timestamp = complain_time
            complain.type = complain_type
            if upload__complain_src:
                complain.src = upload__complain_src
            complain.save()
            return render_to_response('complain_sucess.html', {'user': request.user})
        else:
            return render_to_response('complains.html', {'user': request.user})