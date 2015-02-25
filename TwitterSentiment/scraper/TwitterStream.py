import tweepy
import time
from textblob import TextBlob
from TwitterSentiment.scraper.models import Tweet

class Streamer(tweepy.StreamListener):
	def __init__(self, *args, **kwargs):
		self.hashtags = [
			# Obama
			"obama",
			"barackobama",
			"obamacare",
			"obama-care",
			"patientprotectionandaffordablecareact",
			"ppaca",
			"affordablecareact",
			"aca",
			"obamahealthcare",


			# Fifty Shades
			"fiftyshadesofgrey",
			"50shades",
			"50shadesofgrey",
			"fsog",
			"fiftyshades",
			"mrgreywillseeyounow",
			"mrgrey",
			"fiftyshadesofgreymovie",

			# Bush
			"jebbush",
			"jebbushforpresident",
			"johnellisbush",
			"bushjeb",
			"jebrunningforpresident",
			"jebbrushpresident",
			"jebbush2016",
			"bush2016",

			# Biden
			"joebiden",
			"joebidenforpresident",
			"joebiden2016",

			# Gay marriage
			"gaymarriage",
			"marriageequality",

			# Climate
			"climatechange",
			"warmclima",
			"globalwarming",
			"arcticmelting",
			"antarcticmelting",
			"climateaction",

			# Kygo
			"kygo",
			"kyrre",
			"firestone",

			# Kanye West
			"kanyewest",
			"kanye",
			"sitdownkanye",
			"kanyeomariwest",
			"yeezus",

			# Justin Timberlake
			"justintimberlake",
			"jt202tour",
			"jt",
			"timberbiel",
			"2020experience",
			"jtimberlake",
			"timberlake",
			"jtpresidentofpop",

			# Justin Bieber
			"justinbieber",
			"bieber",
			"justinbieberupdates",
			"jb",
			"beliebers",
			"bieberfamily",
			"belieber",

			# Walmart
			"walmart",
			"wal-mart",

			# Nike
			"nike",
			"freerun2",
			"flyknit",
			"superfly",

			# Valentines
			"valentinesday",
			"valentine",
			"bemyvalentine",
			"vday",
		]
		return super(Streamer, self).__init__(*args, **kwargs)

	def find_hashtag(self, hashtags):
		for tag in hashtags:
			if tag['text'] in self.hashtags:
				return tag['text']
		return False

	def on_status(self, status):
		try:
			if status.coordinates:
				hashtag = self.find_hashtag(status.entities['hashtags'])
				if hashtag:
					place = status.place.full_name.split(",")
					score = TextBlob(status.text)
					Tweet.objects.create(
							tweet_id=status.id,
							hashtag=hashtag,
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

if __name__ == "__main__":
	worker = Worker()
	worker.run()

