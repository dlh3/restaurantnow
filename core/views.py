from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.localflavor import ca
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
from core.models import *

#Index page view
def index(request):
    return render_to_response('core/index.html', context_instance=RequestContext(request))

#Logout page view
def account_logout(request):
    next = reverse('core:index')
    if 'next' in request.GET and request.GET['next'].strip() != '':
        next = request.GET['next']
    logout(request)
    messages.info(request, 'You have logged out')
    return HttpResponseRedirect(next)

#Login page view
def account_login(request):
    next = reverse('core:index')
    if 'next' in request.GET and request.GET['next'].strip() != '':
        next = request.GET['next']
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            messages.error(request, 'Your account is disabled')
    else:
            messages.error(request, 'Please enter a correct username and password. Note that both fields are case-sensitive.')
    return HttpResponseRedirect(next)
