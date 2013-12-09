from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static
from SmartDataApp.controller.admin import register, login, logout, api_user_list, api_user_create, api_user_login, api_user_update, api_user_change_password, api_user_logout
from SmartDataApp.views import *
from SmartDataApp.controller.repair import *
from SmartDataApp.controller.complain import *
from SmartDataApp.controller.community import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^index/$', index),
                       url(r'^register/$', register),
                       url(r'^login/$', login),
                       url(r'^logout/$', logout),
                       url(r'^dashboard/$', dashboard),
                       url(r'^profile/$', profile),
                       url(r'^shine/$', shine),
                       url(r'^upload_image/$', ajax_upload_image),
                       url(r'^like/(?P<id>\d+)/$', ajax_like),
                       url(r'^keep/(?P<id>\d+)/$', ajax_keep),
                       url(r'^delete_picture/(?P<id>\d+)/$', ajax_delete_picture),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r'^generate_captcha/', generate_captcha),
                       url(r'^complain/$', complain),
                       url(r'^repair/$', repair),
                       url(r'^complain/create/$', complain_create),
                       url(r'^repair/create/$', repair_create),
                       url(r'^community/$', add_community),
                       url(r'^deal/complain/$', complain_deal),
                       url(r'^deal/repair/$', repair_deal),
                       url(r'^own_information/$', own_information),
                       url(r'^own_repair/$', own_repair),
                       url(r'^own/complain/$', own_complain),
                       url(r'^api/user/list/$', api_user_list),
                       url(r'^api/user/create/$', api_user_create),
                       url(r'^api/user/login/$', api_user_login),
                       url(r'^api/user/update/$', api_user_update),
                       url(r'^api/complain/create/$', api_complain_create),
                       url(r'^api/user/change_password/$', api_user_change_password),
                       url(r'^api/user/logout/$', api_user_logout),
                       url(r'^complain/response/$', complain_response),
                       url(r'^repair/response/$', repair_response),



) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)