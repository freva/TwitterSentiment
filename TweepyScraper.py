import socket
import db
import tweepy
from django.db.utils import IntegrityError
from textblob import TextBlob
from data.models import Tweet
from time import time
from datetime import datetime

def get_file_names():
	"""
	Returns paths to file depending on host
	"""
	if '3883' in socket.gethostname():
		log_file = '/root/TwitterSentiment/log.txt'
	else:
		log_file = 'log.txt'
	return log_file

class Worker(object):
	def __init__(self):
		self.lang = 'en'
		self.count = 100
		self.log_file = get_file_names()

	def set_query(self, query):
		"""
		Set new query for the worker.

		:param query: query to search for
		"""
		self.query = query

	def get_limit_status(self):	
		"""
		Returns the limit status as integer
		"""
		return self.api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']

	def get_keys(self, user):
		if user == "oyv":
			ACCESS_TOKEN		= "1149321716-4lUNiaF0bDLieONt2ElPRaoC6n0a9qELFQmzxnL"
			ACCESS_TOKEN_SECRET	= "IC0pwj9GoWjVvYp4rHjYesrgrYpgSFloaNFmMeVNPb4"
			CONSUMER_KEY       	= "Hff8xWsJiMpfjoIsUXeWw"
			CONSUMER_SECRET    	= "VbUQ3QKrGj8kimKrNo9ZNbioh5VxPMx4KdH8uB7h9cg"
		elif user == "jon":
			ACCESS_TOKEN        = "2321486359-9o9S5F095e9wOcfLF2j9BEVgpCilaT4tJxnAkUJ"
			ACCESS_TOKEN_SECRET = "FPrE6SifIPOc4Cv4MuiwpKIE2myFmRHKZwPHmwVjtf90t"
			CONSUMER_KEY        = "03wJEEb99nygHwMQWoGeEgiwL"
			CONSUMER_SECRET     = "9u2c2K4V1PLS8eYfjnnFefOIVWhGguztSldNASKYyXcBPSINyL"
		elif user == "val":
			ACCESS_TOKEN 		= "3014396297-AuZwIXKpP9oosXx4XSpbrQ8Pu64QFTdoDVAH9TU"
			ACCESS_TOKEN_SECRET = "NLWiducniEd2y9lgDFQH9LUg3Lwb6caur0RKmwMcPwCWF"
			CONSUMER_KEY        = "DtujIqtFFl9Bg18b2WeMTFPwd"
			CONSUMER_SECRET     = "mpDz7M0ZsU9dowCPmIJePxfqrvEFy4moCyCkgzx4UZPrgffyqN"
		else:
			raise ValueError("Invalid username")
		return ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

	def init_user(self, user):
		"""
		Set API to work with users details

		:param user:
		"""
		ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET = self.get_keys(user)

		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

		self.api = tweepy.API(auth)

	def fetch_tweets(self):
		if not self.since_id:
			return self.api.search(
					q=self.query,
					lang=self.lang,
					count=self.count,
					since_id=self.since_id,
				)
		else:
			return self.api.search(
					q=self.query,
					lang=self.lang,
					count=self.count,
				)

	def save_since_id(self):
		with open(self.state_file, 'w+') as output_file:
			output_file.write(str(self.since_id))

	def load_since_id(self):
		try:
			with open(self.state_file, 'r') as input_file:
				self.since_id = input_file.read().strip()
		except IOError, e:
			self.log("Error loading since ID")
			self.since_id = False

	def get_tweets(self):
		print "Fetching tweets"
		fetched = 0
		self.load_since_id()
		tweets = self.fetch_tweets()
		x = Tweet.objects.all().count()
		self.log("Found %s tweets" %(len(tweets)))
		for t in tweets:
			score = TextBlob(t.text)
			self.since_id = t.id
			try:
				tweet = Tweet(
					tweet_id=t.id,
					text=t.text,
					hashtag=self.query,
					created_at=t.created_at,
					subjectivity=score.subjectivity,
					polarity=score.polarity,
					retweet_count=t.retweet_count,
				)
				if t.coordinates:
					tweet.lat = t.coordinates['coordinates'][-1]
					tweet.lng = t.coordinates['coordinates'][0]

				if t.place:
					tweet.country = t.place.country
					tweet.full_name = t.place.full_name
					tweet.place_id = t.place.id

				tweet.save()
				fetched += 1
			except IntegrityError:
				continue

		self.log("Saved %s tweets" %(Tweet.objects.all().count() - x))
		self.save_since_id()
		return fetched

	def log(self, message, exception=""):
		time = datetime.now().strftime("[%d/%m %H:%M:%S]")
		with open(self.log_file, 'a+') as output_file:
			output_file.write("%s: %s %s\n" %(time, message, exception))

	def set_state_file(self, hashtag):
		if '3883' in socket.gethostname():
			self.state_file = '/root/TwitterSentiment/%s.txt' %(hashtag)
		else:
			self.state_file = '%s.txt' %(hashtag)

	def get_hashtags(self):
		hashtags = [
			"obama",
			"barackobama",
			"obamacare",
			"fiftyshadesofgrey",
			"50shades",
			"50shadesofgrey",
			"fsog",
			"fiftyshades",
			"mrgreywillseeyounow",
			"mrgrey",
			"fiftyshadesofgreymovie",
		]

		for h in hashtags:
			self.set_state_file(h)
			self.log("Working with query: %s" %(h))
			yield "#%s place:96683cc9126741d1" %(h)

	def get_users(self):
		users = ["oyv", "jon", "val"]
		for u in users:
			self.init_user(u)
			yield u

	def run(self):
		for user in self.get_users():
			self.log("Using Twitter with user: %s" %(user))
			while self.get_limit_status() > 0:
				for hashtag in self.get_hashtags():
					self.set_query(hashtag)
					fetched = 100
					while fetched > 50:
						fetched = self.get_tweets()

def main():
	worker = Worker()
	worker.log("Starting TweepyScraper")

	try:
		worker.run()
	except Exception, e:
		worker.log(str(e))

if __name__ == "__main__":
	main()
