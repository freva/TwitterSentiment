import db
from data.models import Tweet
from textblob import TextBlob
from TwitterSearch import TwitterSearch
from time import time


class Scraper(object):
	def __init__(self, twitterSearch, query):
		self.twitter_search = twitterSearch
		self.query = query
		self.endID = ""


	def load_endid(self):
		try:
			with open('state.txt', 'r') as input_file:
				self.endID = input_file.read().strip()
		except IOError, e:
			with open('log.txt', 'a+') as f:
				f.write("FAILED: %s\n" %(e))


	def save_endid(self):
		with open('state.txt', 'w+') as output_file:
			output_file.write(str(self.endID))


	def run(self):
		self.load_endid()
		placeID = self.twitter_search.getTwitterPlaceID("USA", "country")

		for i in xrange(20):
			try:
				#results = self.twitter_search.getTweets(self.query, placeID=placeID, end_id=self.endID)
				results = self.twitter_search.getTweetsWithLocation(self.query, end_id=self.endID)

				for tweet in results["tweets"]:
					sent = TextBlob(tweet["text"])

					Tweet.objects.create(hashtag=self.query, created_at=tweet["datetime"], polarity=sent.polarity,
						subjectivity=sent.subjectivity, lat=tweet["coordinates"][1], lng=tweet["coordinates"][0])
				self.endID = results["low"]
			except Exception, e:
				with open('log.txt', 'a+') as f:
					f.write("FAILED: %s\n" %(e))
		self.save_endid()


def main():
	start = time()
	start_count = Tweet.objects.all().count()
	for user in ["jon", "oyv", "val"]:
		try:
			scraper = Scraper(TwitterSearch(user), "#obama")
			scraper.run()
		except Exception, e:
			with open('log.txt', 'a+') as f:
				f.write("FAILED: %s\n" %(e))
	end_count = Tweet.objects.all().count()
	message = "Fetched %s tweets in %s seconds\n" %(end_count - start_count, round(time() - start, 2))
	with open('log.txt', 'a+') as f:
		f.write(message)


if __name__ == "__main__":
	main()
