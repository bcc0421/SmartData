from django.conf.urls import patterns, url, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from SmartDataApp.controller.admin import *

from SmartDataApp.views import *
from SmartDataApp.controller.repair import *
from SmartDataApp.controller.complain import *
from SmartDataApp.controller.community import *
from SmartDataApp.controller.user_profile import *
from SmartDataApp.controller.express import *
from SmartDataApp.controller.repair_item import *
from SmartDataApp.controller.housekeeping import *
from SmartDataApp.controller.property import *
from SmartDataApp.controller.park import *
from SmartDataApp.controller.update_version import *
from SmartDataApp.pusher.push_api import *






# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from quick_pay_conf_test import quick_pay_conf

urlpatterns = patterns('',
                       url(r'^$', index_test),
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
                       url(r'^enter/community/(?P<id>\d+)/$', enter_community),
                       url(r'^show/image_detail/(?P<id>\d+)/$', show_image_detail),
                       url(r'^delete_picture/(?P<id>\d+)/$', ajax_delete_picture),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r'^generate_captcha/', generate_captcha),
                       url(r'^complain/$', complain),
                       url(r'^express/$', express),
                       url(r'^repair/$', repair),
                       url(r'^complain/create/$', complain_create),
                       url(r'^repair/create/$', repair_create),
                       url(r'^community/$', add_community),
                       url(r'^deal/complain/$', complain_deal),
                       url(r'^complete/complain/$', complain_complete),
                       url(r'^deal/repair/$', repair_deal),
                       url(r'^complete/repair/$', complete_repair),
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
                       url(r'^api/complain/response/$', api_complain_response),
                       url(r'^api/repair/response/$', api_repair_response),
                       url(r'^api/get/user/express/$', api_get_user_express),
                       url(r'^api/own/complain/$', api_own_complain),
                       url(r'^api/own/repair/$', api_own_repair),
                       url(r'^api/show/all_repair/$', api_show_all_repair),
                       url(r'^api/repair/create/$', api_repair_create),
                       url(r'^profile/update/$', profile_update),
                       url(r'^update/own/profile/$', update_own_profile),
                       url(r'^update/own/password/$', update_own_password),
                       url(r'^update/password/$', update_password),
                       url(r'^find/user_express/$', find_user_express),
                       url(r'^add/user_express/$', add_user_express),
                       url(r'^delete/user_express/$', delete_user_express),
                       url(r'^api_user/sign_express/$', api_user_sign_express),
                       url(r'^userself/get_express/$', user_self_get_express),
                       url(r'^express/response/$', express_response),
                       url(r'^api/express/response/$', api_express_response),
                       url(r'^api/user/obtain/express/$', api_user_obtain_express),
                       url(r'^api/complain/deal/$', api_complain_deal),
                       url(r'^api/add/express/record/$', api_add_express_record),
                       url(r'^api/find/inhabitant/$', api_find_inhabitant),
                       url(r'^api/express/delete/$', api_express_delete),
                       url(r'^api/get/community/$', api_get_community),
                       url(r'^api/express/complete/$', api_express_complete),
                       url(r'^manage/repair/item/$', repair_item),
                       url(r'^add/repair_item/$', add_repair_item),
                       url(r'^delete/repair_item/$', delete_repair_item),
                       url(r'^api/repair/deal/$', api_repair_deal),
                       url(r'^api/repair/complete/$', api_repair_complete),
                       url(r'^api/get/repair/item/$', api_get_repair_item),
                       url(r'^api/add/repair/item/record/$', api_add_repair_item_record),
                       url(r'^api/repair/item/delete/$', api_repair_item_delete),
                       url(r'^housekeeping/$', housekeeping),
                       url(r'^manage/housekeeping/item/$', manage_housekeeping_item),
                       url(r'^add/housekeeping_item/$', add_housekeeping_item),
                       url(r'^submit/housekeeping/$', submit_housekeeping),
                       url(r'^delete/housekeeping_item/$', delete_housekeeping_item),
                       url(r'^deal/housekeeping/$', deal_housekeeping),
                       url(r'^complete/housekeeping/$', housekeeping_complete),
                       url(r'^own/housekeeping/$', own_housekeeping),
                       url(r'^housekeeping/response/$', housekeeping_response),
                       url(r'^api/get/worker/list/$', api_get_worker_list),
                       url(r'^modify/housekeeping_item/$', modify_housekeeping_item),
                       url(r'^modify/repair_item/$', modify_repair_item),
                       url(r'^api/show/all_complains/$', api_show_all_complains),
                       url(r'^api/show/all_express/$', api_show_all_express),
                       url(r'^api/own/housekeeping/$', api_own_housekeeping),
                       url(r'^api/user/submit_housekeeping/$', api__user_submit_housekeeping),
                       url(r'^api/housekeeping/response/$', api_housekeeping_response),
                       url(r'^api/housekeeping/deal/$', api_housekeeping_deal),
                       url(r'^api/housekeeping/complete/$', api_housekeeping_complete),
                       url(r'^api/show/all_housekeeping/$', api_show_all_housekeeping),
                       url(r'^api/get/housekeeping_item/$', api_get_housekeeping_item),
                       url(r'^api/add/housekeeping_item/$', api_add_housekeeping_item),
                       url(r'^api/delete/housekeeping_item/$', api_housekeeping_item_delete),
                       url(r'^api/modify/housekeeping_item/$', api_modify_housekeeping_item),
                       url(r'^api/modify/repair_item/$', api_modify_repair_item),
                       url(r'^get/new/dynamic_data/$', get_new_dynamic_data),
                       url(r'^get/detail_data/$', get_detail_data),
                       url(r'^house/pay_fees/$', house_pay_fees),
                       url(r'^api/show/complains_by_status/$', api_show_complains_by_status),
                       url(r'^api/show/repair_by_status/$', api_show_repair_by_status),
                       url(r'^api/show/housekeeping_by_status/$', api_show_housekeeping_by_status),
                       url(r'^api/show/express_by_status/$', api_show_express_by_status),
                       url(r'^parking/fees/$', parking_fees),
                       url(r'^api/get_dynamic_data_num/$', api_get_dynamic_data_num),
                       url(r'^api/get_dynamic_data/$', api_get_dynamic_data),
                       url(r'^api/get_channel_user_id/$', api_get_channel_user_id),
                       url(r'^api/repair/create/android/$', api_repair_create_android),
                       url(r'^api/complain/create/android/$', api_complain_create_android),
                       url(r'^api/complain/complete/$', api_complain_complete),
                       url(r'^api/return_xml/$', return_xml),
                       url(r'^property/$', property_service),
                       url(r'^delete/complain/$', complain_delete),
                       url(r'^delete/repair/$', repair_delete),
                       url(r'^delete/housekeeping/$', housekeeping_delete),
                       url(r'^user/pay_property_by_month/$', user_pay_property_by_month),
                       url(r'^property/user_pay_online/$', property_user_pay_online),
                       url(r'^own/housekeeping_detail/$', housekeeping_detail),
                       url(r'^worker_deal/repair/$', worker_deal_repair),
                       url(r'^worker_deal/complain/$', worker_deal_complain),
                       url(r'^user/prepare_pay_property_fees/$', user_prepare_pay_fee),
                       url(r'^user/property/verifyParking/$', user_property_verifyParking),
                       url(r'^community/notification/$', community_notification),
                       url(r'^add/notification/$', add_notification),
                       url(r'^notification/detail/$', notification_detail),
                       url(r'^modify/notification/$', modify_notification),
                       url(r'^delete/notification/$', delete_notification),
                       url(r'^recharge/$', user_recharge),
                       url(r'^decide/recharge/$', decide_recharge),
                       url(r'^api_worker/deal/repair/$', api_worker_deal_repair),
                       url(r'^api_worker/deal/complain/$', api_worker_deal_complain),
                       url(r'^property/parkingOrder/$', property_parking_Order),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
