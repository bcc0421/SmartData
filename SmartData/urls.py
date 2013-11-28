from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static

from SmartDataApp.views import *



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

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)