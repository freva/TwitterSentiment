from django.core.management.base import BaseCommand, CommandError
from TwitterSentiment.scraper.models import *
from TwitterSentiment.stats.models import *
from textblob import TextBlob
from time import time
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):	
	def handle(self, *args, **kwargs):
		for t in TagStats.objects.all():
			t.toggle()
		for c in CaseStats.objects.all():
			c.toggle()

		for t in Tag.objects.all():
			x = TagStats.objects.filter(tag=t).last()
			x.toggle()

		for c in Case.objects.all():
			x = CaseStats.objects.filter(case=c).last()
			x.toggle()