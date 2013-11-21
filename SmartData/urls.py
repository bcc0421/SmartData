from django.conf.urls import patterns, url
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
                       url(r'^ajax_upload_image/$', ajax_upload_image),
                       url(r'^like/(?P<id>.+)/$', ajax_like),
                       url(r'^keep/(?P<id>.+)/$', ajax_keep),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)