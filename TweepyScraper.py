import socket
import db
import tweepy
from django.db.utils import IntegrityError
from textblob import TextBlob
from data.models import Tweet
from time import time

def get_file_names():
	"""
	Returns paths to file depending on host
	"""
	if '3883' in socket.gethostname():
		log_file = '/root/TwitterSentiment/log.txt'
		state_file = '/root/TwitterSentiment/state.txt'
	else:
		log_file = 'log.txt'
		state_file = 'state.txt'
	return log_file, state_file

class Worker(object):
	def __init__(self):
		self.lang = 'en'
		self.count = 100
		self.log_file, self.state_file = get_file_names()

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
				

	def save_since_id(self):
		print "Saving since id"
		with open(self.state_file, 'w+') as output_file:
			output_file.write(str(self.since_id))

	def load_since_id(self):
		print "Loading since id"
		try:
			with open(self.state_file, 'r') as input_file:
				self.since_id = input_file.read().strip()
		except IOError, e:
			print "FAILED: %s" %(e)
			self.since_id = False

	def run(self):
		while self.get_limit_status() > 2:
			self.load_since_id()
			tweets = self.fetch_tweets()
			x = Tweet.objects.all().count()
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
					)
					if t.coordinates:
						tweet.lat = t.coordinates['coordinates'][-1]
						tweet.lng = t.coordinates['coordinates'][0]

					if t.place:
						tweet.country = t.place.country
						tweet.full_name = t.place.full_name
						tweet.place_id = t.place.id

					tweet.save()

				except IntegrityError, e:
					print "FAILED: %s" %(e)
					continue

			print "Saved %s tweets" %(Tweet.objects.all().count() - x)
			self.save_since_id()

def main():
	worker = Worker()

	worker.init_user("oyv")
	worker.set_query('#obama')
	worker.run()

	worker.init_user("jon")
	worker.set_query("#barackobama")
	worker.run()

if __name__ == "__main__":
	main()
