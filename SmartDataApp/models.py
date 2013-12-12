#coding:utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Community(models.Model):
    title = models.CharField(max_length=50, null=False, unique=True, blank=False)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.title


class Picture(models.Model):
    author = models.ForeignKey(User, null=True)
    title = models.CharField(max_length=100, null=False, unique=True, blank=False)
    comment = models.CharField(max_length=255, null=True)
    src = models.ImageField(upload_to='uploads/%Y/%m/%d', null=True)
    timestamp_add = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)
    like = models.IntegerField(default=0)
    keep = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ProfileDetail(models.Model):
    profile = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d')
    phone_number = models.CharField(max_length=11, null=True)
    community = models.ForeignKey(Community, null=True)
    #pictures = models.ManyToManyField(Picture, null=True)
    floor = models.CharField(max_length=20, null=True)
    gate_card = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number


class Complaints(models.Model):
    content = models.CharField(max_length=1000, null=True, blank=True, default='')
    author = models.CharField(blank=True, null=True, max_length=250, default='')
    timestamp = models.DateTimeField(default=timezone.now)
    handler = models.ForeignKey(User, null=True)
    pleased = models.IntegerField(default=0)
    type = models.CharField(max_length=200)
    status = models.IntegerField(default=1)
    src = models.ImageField(upload_to='uploads/%Y/%m/%d', null=True)
    pleased_reason = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.content


class Repair(models.Model):
    content = models.CharField(max_length=250, null=True, blank=True, default='')
    author = models.CharField(blank=True, null=True, max_length=250, default='')
    timestamp = models.DateTimeField(default=timezone.now)
    handler = models.ForeignKey(User, null=True)
    pleased = models.IntegerField(default=0)
    type = models.CharField(max_length=200)
    status = models.IntegerField(default=1)
    src = models.ImageField(upload_to='uploads/%Y/%m/%d', null=True)
    pleased_reason = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.content


class Express(models.Model):
    author = models.ForeignKey(ProfileDetail, null=True)
    arrive_time = models.DateTimeField(default=timezone.now)
    get_time = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    handler = models.ForeignKey(User, null=True)

    def __str__(self):
        return self.type