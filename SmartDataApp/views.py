#coding:utf-8
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.contrib.auth import authenticate, login


def index(request):
    return render_to_response('index.html')


@transaction.autocommit
@csrf_protect
def register(request):
    if request.method == 'GET':
        c = {}
        c.update(csrf(request))
        return render_to_response('register.html', c)
    elif request.method == 'POST':
        email = request.POST.get(u'email', None)
        username = request.POST.get(u'username', None)
        password = request.POST.get(u'password', None)
        if email and username and password:
            user = User.objects.get_or_create(username=username)[0]
            if password:
                user.password = password
            if email:
                user.email = email
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                return redirect(index)
