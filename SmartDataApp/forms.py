#coding:utf-8
from django.core.validators import RegexValidator

__author__ = 'Administrator'

from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    phone_number = forms.CharField(label=u'手机号码', required=True,
                                   validators=[
                                       RegexValidator(r'^(1[0-9][0-9])\d{8}$',
                                                      u'请输入正确的手机号码！')],
                                   widget=forms.TextInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': '手机号码',
                                       'required': 'required'
                                   }))
    username = forms.CharField(label=u'用户名', required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': '用户名',
                                   'required': 'required'
                               }))
    password = forms.CharField(label=u'密　码', required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': '密　码',
                                   'required': 'required'
                               }))
    email = forms.EmailField(label=u'邮　箱', required=False,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': '邮　箱'
                             }))
    captcha = CaptchaField(label=u'验证码', required=False, error_messages={'invalid': u'验证码错误'})