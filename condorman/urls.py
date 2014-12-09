from django.conf.urls.defaults import patterns, include, url
from condorman.models import CondorUser

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('condorman.views',
    url(r'^$', 'index'),
    url(r'^test$', 'test'),
    url(r'^add/$', 'add'),
    url(r'^modify/$', 'add'),
    url(r'^process/$', 'process'),
    url(r'^log/$', 'log'),
)

urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
