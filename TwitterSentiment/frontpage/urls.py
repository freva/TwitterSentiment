from django.conf.urls import patterns, url

urlpatterns = patterns('TwitterSentiment.frontpage.views',
	url(r'^$', 'home', name='home'),
	url(r'^get_hashtag/$', 'get_hashtag', name='get_hashtag'),
    url(r'^get_tokens/$', 'get_tokens', name='get_tokens'),
    url(r'^graph/$', 'graph_hashtag', name='graph_hashtag'),
)