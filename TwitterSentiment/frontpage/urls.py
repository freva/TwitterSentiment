from django.conf.urls import patterns, url

urlpatterns = ('TwitterSentiment.frontpage.views',
	url(r'^$', 'home', name='home'),
)
