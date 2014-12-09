from django.conf.urls.defaults import include, url, patterns
from django.conf.urls.defaults import handler404, handler500
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # hack to use admin widgets
    url(r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    #
#    url(r'^polls/', include('polls.urls')),
    url(r'^condorman/', include('condorman.urls')),
    url(r'media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    )

                     
