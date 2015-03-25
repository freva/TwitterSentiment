from django.core.management.base import BaseCommand, CommandError
from TwitterSentiment.scraper.models import *
from textblob import TextBlob
from time import time
import tweepy
import logging
import re

logger = logging.getLogger(__name__)

class Command(BaseCommand):	
	def handle(self, *args, **kwargs):
		""" 
		Start the tweet fetcher
		Usage: python manage.py fetch_tweets
		"""
		logger.info('Starting tweet fetcher')
		worker = Worker()
		worker.run()

class Streamer(tweepy.StreamListener):
	def __init__(self, *args, **kwargs):
		"""
		Initializes the streamer.
		"""
		self.last_id = self.find_last_id()
		self.tweets_parsed = 0
		self.hashtags = [t.encode("ascii") for t in Tag.objects.all().values_list('name', flat=True)]
		return super(Streamer, self).__init__(*args, **kwargs)

	def find_last_id(self):
		"""
		Finds last id used in tweets.
		"""
		try:
			return max(Tweet.objects.all().values_list('id', flat=True))
		except ValueError:
			logger.exception('Failed finding the last tweet id')
			return 0

	def find_hashtag(self, hashtags):
		"""
		Check if the tweet contains one of the recording hashtags
		"""
		for tag in hashtags:
			if tag['text'].lower() in self.hashtags:
				return Tag.objects.get(name__iexact=tag['text'])
		return False

	def on_status(self, status):
		try:
			self.tweets_parsed += 1
			if self.tweets_parsed % 10000 == 0:
				logger.info('Searched through %s tweets' %(self.tweets_parsed))
		except Exception as e:
			logger.exception('Failed counting tweets parsed')
		try:
			if status.coordinates:
				if status.entities['hashtags']:
					text = self.purgeEmoji(status.text)
					hashtag = self.find_hashtag(status.entities['hashtags'])
					if hashtag:
						try:
							place = status.place.full_name.split(",")
						except:
							place = ""
						score = TextBlob(text)
						self.last_id += 1
						Tweet.objects.create(
								id=self.last_id,
								tweet_id=status.id,
								text=text,
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
			try:
				logger.info("Text: %s" %(status.text))
			except:
				pass
			logger.exception('Exception raised when parsing tweet')

	def purgeEmoji(self, text):
		try:
			# Wide UCS-4 build
			myre = re.compile(u'['
				u'\U0001F300-\U0001F64F'
				u'\U0001F680-\U0001F6FF'
				u'\u2600-\u26FF\u2700-\u27BF]+', 
				re.UNICODE)
		except re.error:
			# Narrow UCS-2 build
			myre = re.compile(u'('
				u'\ud83c[\udf00-\udfff]|'
				u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
				u'[\u2600-\u26FF\u2700-\u27BF])+', 
				re.UNICODE)
		return myre.sub('', text)


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

