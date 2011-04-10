from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('project.core.urls', namespace="core")),
    (r'^pos/', include('project.pos.urls', namespace="pos")),
    (r'^web/', include('project.web.urls', namespace="web")),
    (r'^admin/', include(admin.site.urls)),
)
    # Example:
    # (r'^project/', include('project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

