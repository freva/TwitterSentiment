from django.db import models

class Tweet(models.Model):
	tweet_id = models.CharField(max_length=200, unique=True)
	hashtag = models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField(blank=True, null=True)
	retweet_count = models.IntegerField(blank=True, null=True, default=0)
	favorite_count = models.IntegerField(blank=True, null=True, default=0)
	lat = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3)
	lng = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3)
	state = models.CharField(max_length=3, blank=True, null=True)
	city = models.CharField(max_length=50, blank=True, null=True)
	subjectivity = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)
	polarity = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)

	def __unicode__(self):
		return "#%s" %(self.hashtag)

	def get_coordinates(self):
		return "%s, %s" %(self.lat, self.lng)