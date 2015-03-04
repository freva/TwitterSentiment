from TwitterSentiment.scraper.models import Tweet, Tag, Case

class Cases(object):
	def __init__(self, case):
		self.name = case
		self.hashtags = 0
		self.tweets = 0
		self.subjectivity = 0
		self.polarity = 0

		temp_tweets = 0
		temp_tag = False
		temp_tag_tweets = 0

		for tag in case.tags.all():
			self.hashtags += 1
			temp_tweets = 0

			for tweet in Tweet.objects.filter(tag=tag):
				temp_tweets += 1
				self.subjectivity += tweet.subjectivity
				self.polarity += tweet.polarity

			if not temp_tag:
				temp_tag = tag
				temp_tag_tweets = temp_tweets
			elif temp_tweets > temp_tag_tweets:
				temp_tag = tag
				temp_tag_tweets = temp_tweets

			self.tweets += temp_tweets
		self.most_popular_hashtag = temp_tag

		try:
			self.subjectivity = round(float(self.subjectivity) / float(self.tweets), 2)
		except ZeroDivisionError:
			self.subjectivity = 0

		try:
			self.polarity = round(float(self.polarity) / float(self.tweets), 2)
		except ZeroDivisionError:
			self.polarity = 0

class Hashtags(object):
	def __init__(self, hashtag):
		try:
			self.case = Case.objects.filter(tags=hashtag)[0]
		except:
			self.case = ""
		self.name = hashtag
		self.tweets = 0
		self.subjectivity = 0
		self.polarity = 0

		for tweet in Tweet.objects.filter(tag=hashtag):
			self.tweets += 1
			self.subjectivity += tweet.subjectivity
			self.polarity += tweet.polarity

		try:
			self.subjectivity = round(float(self.subjectivity) / float(self.tweets), 2)
		except ZeroDivisionError:
			self.subjectivity = 0

		try:
			self.polarity = round(float(self.polarity) / float(self.tweets), 2)
		except ZeroDivisionError:
			self.polarity = 0