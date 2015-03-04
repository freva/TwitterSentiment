from django.core.management.base import BaseCommand, CommandError
from TwitterSentiment.scraper.models import *
from TwitterSentiment.stats.models import *
from os import system
from time import time
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		self.stop_scraper()
		logger.info("Starting stats calculator")
		start = time()
		logger.info("Running: calculate_case_stats()")
		self.calculate_case_stats()
		logger.info("Completed: calculate_case_stats() in %s seconds" %(round(time() - start, 2)))

		start = time()
		logger.info("Running: calculate_tag_stats()")
		self.calculate_tag_stats()
		logger.info("Completed: calculate_tag_stats() in %s seconds" %(round(time() - start, 2)))
		logger.info("Shutting down stats calculator")
		self.start_scraper()

	def stop_scraper(self):
		logger.info("Stopping scraper")
		system("supervisorctl stop twitter")

	def start_scraper(self):
		logger.info("Starting scraper")
		system("supervisorctl start twitter")

	def calculate_case_stats(self):
		for c in Case.objects.all():
			self.parse_case(c)

	def parse_case(self, case):
		tweets, polarity, subjectivity, hashtags = 0, 0, 0, 0
		temp_tweets, temp_tag_tweets = 0, 0
		temp_tag = False

		for tag in case.tags.all():
			hashtags += 1
			temp_tweets = 0

			for tweet in Tweet.objects.filter(tag=tag):
				temp_tweets += 1
				subjectivity += tweet.subjectivity
				polarity += tweet.polarity

			if not temp_tag:
				temp_tag = tag
				temp_tag_tweets = temp_tweets
			elif temp_tweets > temp_tag_tweets:
				temp_tag = tag
				temp_tag_tweets = temp_tweets

			tweets += temp_tweets

		try:
			subjectivity = round(float(subjectivity) / float(tweets), 2)
		except ZeroDivisionError:
			subjectivity = 0

		try:
			polarity = round(float(polarity) / float(tweets),2)
		except ZeroDivisionError:
			polarity = 0

		CaseStats.objects.create(
				case=case,
				hashtags=hashtags,
				tweets=tweets,
				subjectivity=subjectivity,
				polarity=polarity,
				most_used_hashtag=temp_tag
			)

	def calculate_tag_stats(self):
		for t in Tag.objects.all():
			self.parse_tag(t)

	def parse_tag(self, tag):
		try:
			case = Case.objects.filter(tags=tag)[0]
		except:
			case = False

		tweets, subjectivity, polarity = 0, 0, 0
		for tweet in Tweet.objects.filter(tag=tag):
			tweets += 1
			subjectivity += tweet.subjectivity
			polarity += tweet.polarity

		try:
			subjectivity = round(float(subjectivity) / float(tweets), 2)
		except ZeroDivisionError:
			subjectivity = 0

		try:
			polarity = round(float(polarity) / float(tweets), 2)
		except ZeroDivisionError:
			polarity = 0

		if case:
			TagStats.objects.create(
					case=case,
					tag=tag,
					tweets=tweets,
					subjectivity=subjectivity,
					polarity=polarity,
				)
		else:
			TagStats.objects.create(
					tag=tag,
					tweets=tweets,
					subjectivity=subjectivity,
					polarity=polarity
				)