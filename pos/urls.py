from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, password_change
from django.conf import settings
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    url(r'^$', 'pos.views.index', name='index'),
    # Example:
    # (r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
