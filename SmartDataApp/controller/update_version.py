
from django.http import HttpResponse
from django.template import loader, Context

def return_xml(request):
    t = loader.get_template("version.xml")
    c = Context()
    return HttpResponse(t.render(c), mimetype="text/xml")
    #return HttpResponse(simplejson.dumps(response_data), content_type='application/json')