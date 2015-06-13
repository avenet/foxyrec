from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'app.views.inicio', name='home'),
                       url(r'inicio/$', 'app.views.inicio', name='inicio'),
                       url(r'^loop/(?P<user_id>[^/]+)/$', 'app.views.loop', name='loop'),
                       )
