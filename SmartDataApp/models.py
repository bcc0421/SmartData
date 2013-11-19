#coding:utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Community(models.Model):
    title = models.CharField(max_length=50, null=False, unique=True, blank=False)

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
    profile = models.ForeignKey(User)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d')
    cell_phone = models.CharField(max_length=11, null=True)
    community = models.ForeignKey(Community, null=True)
    pictures = models.ManyToManyField(Picture, null=True)

    def __str__(self):
        return self.cell_phone
