from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ajax.views',
    url(r'^(?P<function>[a-z0-9_\\.]+)/$', 'call', name='call'),
)
