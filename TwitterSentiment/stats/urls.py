from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('TwitterSentiment.stats.views',
	url(r'^cases/$', 'cases', name='cases'),
	url(r'^hashtags/$', 'hashtags', name='hashtags'),
)