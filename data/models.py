from django.db import models

class Tweet(models.Model):
	tweet_id = models.CharField(max_length=200, unique=True)
	hashtag = models.CharField(max_length=50, blank=True, null=True)
	text = models.CharField(max_length=200, blank=True, null=True)
	created_at = models.DateTimeField()
	retweet_count = models.IntegerField(blank=True, null=True, default=0)
	subjectivity = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)
	polarity = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)
	lat = models.DecimalField(blank=True, null=True, max_digits=18, decimal_places=15)
	lng = models.DecimalField(blank=True, null=True, max_digits=18, decimal_places=15)
	country = models.CharField(blank=True, null=True, max_length=200)
	place_type = models.CharField(blank=True, null=True, max_length=200)
	full_name = models.CharField(blank=True, null=True, max_length=200)
	place_id = models.CharField(blank=True, null=True, max_length=200)

	def get_coordinates(self):
		return "%s, %s" %(self.lat, self.lng)

	def __unicode__(self):
		return self.hashtag
