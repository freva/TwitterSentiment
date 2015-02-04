import db
import sys
from data.models import Tweet
from datetime import datetime
from textblob import TextBlob
import dateutil.parser
import time
import twitter
from TwitterSearch import getTweets, getTwitterPlaceID

class Scraper(object):
	def __init__(self, 
			CONSUMER_KEY, CONSUMER_SECRET,
			OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
			hashtag
		):
		self.CONSUMER_KEY = CONSUMER_KEY
		self.CONSUMER_SECRET = CONSUMER_SECRET
		self.OAUTH_TOKEN = OAUTH_TOKEN
		self.OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRET
		self.hashtag = hashtag

	def start_twitter(self):
		auth = twitter.oauth.OAuth(
				self.OAUTH_TOKEN,
				self.OAUTH_TOKEN_SECRET,
				self.CONSUMER_KEY,
				self.CONSUMER_SECRET,
			)
		self.twitter_api = twitter.Twitter(auth=auth)

	def searchTweetsWithLocation(self, query, start_id='', end_id=''):
		search_results = self.twitter_api.search.tweets(q=query, lang='en', result_type='recent', count=100, since_id=start_id, max_id=end_id)
		statuses, results = search_results['statuses'], []

		for tweet in statuses:
			timestamp = int(time.mktime(dateutil.parser.parse(tweet["created_at"]).timetuple()))
			text = tweet["text"].encode('ascii', errors='ignore').replace('\n', ' ')

			if tweet["coordinates"] is not None and tweet["coordinates"]["coordinates"] != [0.0, 0.0]:
				results.append({"id": tweet["id"], "tweetTime": timestamp, "text": text, "coordinates": tweet["coordinates"]})
		return {"low": statuses[-1]["id"], "high": statuses[0]["id"], "tweets": results}

	def load_endid(self):
		try:
			with open('%s.txt' %(self.CONSUMER_KEY), 'r') as input_file:
				self.endid = input_file.read().strip()
		except IOError:
			self.endid = ""

	def save_endid(self):
		with open('%s.txt' %(self.CONSUMER_KEY), 'w+') as output_file:
			output_file.write(str(self.endid))

	def run(self):
		self.load_endid()
		placeID = getTwitterPlaceID("USA", "country")
		for i in xrange(10):
			results = getTweets(self.hashtag, placeID=placeID, end_id=self.endid)
	        for tweet in results["tweets"]:
	            sent = TextBlob(tweet["text"])

	            Tweet.objects.create(hashtag=self.hashtag, created_at=datetime.fromtimestamp(tweet["tweetTime"]), polarity=sent.polarity, subjectivity=sent.subjectivity, lat=tweet["coordinates"][-1], lng=tweet["coordinates"][0])
	        endid = results["low"]
		self.save_endid()

def get_user(option):
	if option == 1:
		OAUTH_TOKEN = "2321486359-9o9S5F095e9wOcfLF2j9BEVgpCilaT4tJxnAkUJ"
		OAUTH_TOKEN_SECRET = "FPrE6SifIPOc4Cv4MuiwpKIE2myFmRHKZwPHmwVjtf90t"
		CONSUMER_KEY = "03wJEEb99nygHwMQWoGeEgiwL"
		CONSUMER_SECRET = "9u2c2K4V1PLS8eYfjnnFefOIVWhGguztSldNASKYyXcBPSINyL"
	elif option == 2:
		OAUTH_TOKEN = "1149321716-4lUNiaF0bDLieONt2ElPRaoC6n0a9qELFQmzxnL"
		OAUTH_TOKEN_SECRET = "IC0pwj9GoWjVvYp4rHjYesrgrYpgSFloaNFmMeVNPb4"
		CONSUMER_KEY = "Hff8xWsJiMpfjoIsUXeWw"
		CONSUMER_SECRET = "VbUQ3QKrGj8kimKrNo9ZNbioh5VxPMx4KdH8uB7h9cg"


	return CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def main(option):
	for i in [1, 2]:
		scrape(i)

def scrape(option):
	CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET = get_user(option)
	scraper = Scraper(
			CONSUMER_KEY,
			CONSUMER_SECRET,
			OAUTH_TOKEN,
			OAUTH_TOKEN_SECRET,
			"#obama"
		)
	scraper.start_twitter()
	scraper.run()

if __name__ == "__main__":
	main()
