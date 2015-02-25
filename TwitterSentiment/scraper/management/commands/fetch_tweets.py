from django.core.management.base import BaseCommand, CommandError
from TwitterSentiment.scraper.models import *
from textblob import TextBlob
import time
import tweepy

class Command(BaseCommand):	
	def handle(self, *args, **kwargs):
		worker = Worker()
		worker.run()

class Streamer(tweepy.StreamListener):
	def __init__(self, *args, **kwargs):
		self.hashtags = [t.encode("ascii") for t in Tag.objects.all().values_list('name', flat=True)]
		return super(Streamer, self).__init__(*args, **kwargs)

	def find_hashtag(self, hashtags):
		for tag in hashtags:
			if tag['text'].lower() in self.hashtags:
				return Tag.objects.get(name__iexact=tag['text'])
		return False

	def on_status(self, status):
		try:
			if status.coordinates:
				if status.entities['hashtags']:
					hashtag = self.find_hashtag(status.entities['hashtags'])
					if hashtag:
						place = status.place.full_name.split(",")
						score = TextBlob(status.text)
						Tweet.objects.create(
								tweet_id=status.id,
								tag=hashtag,
								hashtag=hashtag.name,
								created_at=status.created_at,
								retweet_count=status.retweet_count,
								favorite_count=status.favorite_count,
								lat=round(status.coordinates['coordinates'][-1], 3),
								lng=round(status.coordinates['coordinates'][0], 3),
								city=place[0],
								state=place[-1].strip(),
								polarity=score.polarity,
								subjectivity=score.subjectivity
							)
		except Exception as e:
			print e

class Worker(object):
	def __init__(self):
		self.initialize_user()

	def initialize_user(self):
		self.ACCESS_TOKEN = "1149321716-4lUNiaF0bDLieONt2ElPRaoC6n0a9qELFQmzxnL"
		self.ACCESS_TOKEN_SECRET = "IC0pwj9GoWjVvYp4rHjYesrgrYpgSFloaNFmMeVNPb4"
		self.CONSUMER_KEY = "Hff8xWsJiMpfjoIsUXeWw"
		self.CONSUMER_SECRET = "VbUQ3QKrGj8kimKrNo9ZNbioh5VxPMx4KdH8uB7h9cg"
		self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
		self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

	def run(self):
		while 1:
			stream = tweepy.Stream(self.auth, Streamer())
			stream.filter(
					languages=['en',],
					locations=[-125.3,25.5,-66.8,48.9],
				)
