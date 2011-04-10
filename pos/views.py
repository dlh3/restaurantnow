from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from core.models import *

def index(request):
    return render_to_response('pos/index.html', {}, context_instance=RequestContext(request))

