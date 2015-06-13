from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.inicio', name='home'),
    url(r'inicio/$', 'app.views.inicio', name='inicio'),
    url(r'^loop/(?P<user_id>[^/]+)/$', 'app.views.loop', name='loop'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
)
