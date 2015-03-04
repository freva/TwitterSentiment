from django.conf.urls import patterns, url

urlpatterns = patterns('TwitterSentiment.frontpage.views',
	url(r'^$', 'home', name='home'),
	url(r'^get_hashtag/$', 'get_hashtag', name='get_hashtag'),
)