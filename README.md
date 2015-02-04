# TwitterSentiment
TMA4851 Big Data project - Group 1

$ pip install python-dateutil

$ pip install textblob

$ pip install python

$ pip install Django==1.7.4

## Database operations

    Tweet(models.Model):
    	hashtag = models.CharField(max_length=50, blank=True, null=True)
		created_at = models.DateTimeField()
		subjectivity = models.DecimalField(max_digits=5, decimal_places=3)
		polarity = models.DecimalField(max_digits=5, decimal_places=3)
		x = models.DecimalField(max_digits=18, decimal_places=15)
		y = models.DecimalField(max_digits=18, decimal_places=15)

	Tweet.objects.create(created_at=date, polarity=1.1, subjectivity=1.2, x=123.123, y=67.134)
	Tweet.objects.filter(polarity__gte=1.1)
	Tweet.objects.exclude(polarity__lt=1.1)
	Tweet.objects.all()
	Tweet.objects.filter(polarity__gte=1.1).count()
	Tweet.objects.filter(created_at=datetime.today()).delete()

## Twitter API:

![API overview](http://mike.teczno.com/img/raffi-krikorian-map-of-a-tweet.png)
