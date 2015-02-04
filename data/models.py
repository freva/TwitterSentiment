from django.db import models

class Tweet(models.Model):
	hashtag = models.CharField(max_length=50, blank=True, null=True)
	created_at = models.DateTimeField()
	subjectivity = models.DecimalField(max_digits=5, decimal_places=3)
	polarity = models.DecimalField(max_digits=5, decimal_places=3)
	x = models.DecimalField(max_digits=18, decimal_places=15)
	y = models.DecimalField(max_digits=18, decimal_places=15)
