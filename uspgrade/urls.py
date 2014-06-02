from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', 'uspgrade.views.home', name='home'),
    url(r'^login$', 'uspgrade.views.entrar', name='login'),
    url(r'^sair$', 'uspgrade.views.sair', name='sair'),
    url(r'^sobre$', 'uspgrade.views.sobre', name='sobre'),
    url(r'^fazer-sugestao$', 'uspgrade.views.fazer_sugestao', name='fazer-sugestao'),
    url(r'^cadastro$', 'uspgrade.views.cadastro', name='cadastro'),
    url(r'^buscar$', 'uspgrade.views.buscar', name='buscar'),
    url(r'^sugestao/([-\w]+)$', 'uspgrade.views.sugestao', name='sugestao'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
