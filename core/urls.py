from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, password_change
from django.conf import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    url(r'^$', 'core.views.index', name='index'),
    url(r'^favicon.ico$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'path': 'favicon.ico'}, name="favicon"),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}, name="static"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}, name="foodimages"),
    url(r'^logout/$', 'core.views.account_logout', name='logout'),
    url(r'^login/$', 'core.views.account_login', name='login'),

    # Example:
    # (r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
