from django.conf.urls import patterns, url, include
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'app.views.inicio', name='home'),
                       url(r'inicio/$', 'app.views.inicio', name='inicio'),
                       url(r'^loop/(?P<user_id>[^/]+)/$', 'app.views.loop', name='loop'),
                       url(r'^accounts/', include('allauth.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
