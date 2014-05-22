from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', 'uspgrade.views.home', name='home'),
    url(r'^sobre$', 'uspgrade.views.sobre', name='sobre'),
    url(r'^fazer-sugestao$', 'uspgrade.views.fazer_sugestao', name='fazer-sugestao'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
