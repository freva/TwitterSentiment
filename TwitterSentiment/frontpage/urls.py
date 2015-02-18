from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('TwitterSentiment.frontpage.views',
	url(r'^$', 'home', name='home'),
	url(r'^get_hashtag/$', 'get_hashtag', name='get_hashtag'),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)