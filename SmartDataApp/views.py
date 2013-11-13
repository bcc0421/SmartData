#coding:utf-8
from django.shortcuts import render_to_response
from django.contrib.auth.models import User


def index(request):
    return render_to_response('index.html')


def login(request):
    pass


def register(request):
    if request.method == 'GET':
        return render_to_response('register.html')
    elif request.method == 'POST':
        username = 'username'
        password = 'password'
        email = 'email'
        user = User.objects.create_user(username, email, password)
        user.save()