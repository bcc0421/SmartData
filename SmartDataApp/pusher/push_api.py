from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import simplejson
from SmartDataApp.controller.admin import return_error_response
from SmartDataApp.views import convert_session_id_to_user
from SmartDataApp.models import ProfileDetail

@transaction.atomic
@csrf_exempt
def api_get_channel_use_id(request):
    convert_session_id_to_user(request)
    if request.method != u'POST':
        return return_error_response()
    elif 'application/json' in request.META['CONTENT_TYPE'].split(';'):
        data = simplejson.loads(request.body)
        channel_id = data.get("channel_id", None)
        user_id = data.get("user_id", None)
        if channel_id and user_id:
            profile = ProfileDetail.objects.get(profile=request.user)
            profile.device_chanel_id = channel_id
            profile.device_user_id = user_id
            profile.save()
            return HttpResponse(simplejson.dumps({'success': True, 'info': '绑定成功'}), content_type='application/json')
        else:
            return HttpResponse(simplejson.dumps({'success': False, 'info': '没有传入相关信息'}), content_type='application/json')
