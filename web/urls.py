from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, password_change
from django.conf import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    url(r'^$', 'web.views.index', name='index'),
    url(r'menu/$', 'web.views.menu', name='menu'),
    url(r'checkout/$', 'web.views.checkout', name='checkout'),
    url(r'previous/$', 'web.views.previous', name='previous'),
    url(r'register/$', 'web.views.register', name='register'),
    url(r'delete/$', 'web.views.delete', name='delete'),
    url(r'^profile/$', 'web.views.profile', name='profile'),
    url(r'^nameserv/$', 'web.views.nameserv', name='nameserv'),
    url(r'^directions/$', 'web.views.directions', name='directions'),
    url(r'^members/$', 'web.views.directions', name='members'),
    url(r'^specials/$', 'web.views.directions', name='specials'),

    # Example:
    # (r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
