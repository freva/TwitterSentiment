from django.conf.urls import patterns, url

urlpatterns = patterns('TwitterSentiment.frontpage.views',
	url(r'^$', 'home', name='home'),
)
