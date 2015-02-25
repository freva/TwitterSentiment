from django.core.management.base import BaseCommand, CommandError
from TwitterSentiment.scraper.models import *
from time import time
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):	
	def handle(self, *args, **kwargs):
		logger.info("Refactoring tweets")
		start = time()
		tweets = Tweet.objects.filter(tag__isnull=True)
		logger.info("Found %s tweets in %s seconds that need refactoring" %(tweets.count(), round(time() - start, 1)))
		start = time()
		logger.info("Working...")
		for t in tweets:
			self.refactor(t)
		tweets_left = Tweet.objects.filter(tag__isnull=True).count()
		logger.info("Refactored %s tweets in %s seconds." %(tweets.count() - tweets_left, round(time() - start, 1))) 

	def refactor(self, t):
		try:
			t.tag = Tag.objects.get(name__iexact=t.hashtag)
			t.save()
		except:
			logger.warning("Failed to refactor: %s" %(t.hashtag))
			pass
