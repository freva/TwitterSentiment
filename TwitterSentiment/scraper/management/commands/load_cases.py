from django.core.management.base import BaseCommand, CommandError
from TwitterSentiment.scraper.models import *
from time import time
import logging
logger = logging.getLogger(__name__)

CASES = {
	'Valentines Day': [
		'valentinesday',
		'valentine',
		'bemyvalentine',
		'vday'	
	],
	'Barack Obama': [
		"obama",
		"barackobama",
		"obamacare",
		"obama-care",
		"patientprotectionandaffordablecareact",
		"ppaca",
		"affordablecareact",
		"aca",
		"obamahealthcare",			
	],
	'Fifty Shades of Grey': [
		'fiftyshadesofgrey',
		'50shades',
		'50shadesofgrey',
		'fsog',
		'fiftyshades',
		'mrgreywillseeyounow',
		'mrgrey',
		'fiftyshadesofgreymovie',
	],
	'John Ellis Bush': [
		'jebbush',
		'jebbushforpresident',
		'johnellisbush',
		'bushjeb',
		'jebrunningforpresident',
		'jebbushpresident',
		'jebbush2016',
		'bush2016',
	],
	'Joe Biden': [
		'joebiden',
		'joebidenforpresident',
		'joebiden2016',
	],
	'Gay Marriage': [
		'gaymarriage',
		'marriageequality',
	],
	'Climate': [
		'climatechange',
		'warmclima',
		'globalwarming',
		'arcticmelting',
		'antarcticmelting',
		'climateaction',
	],
	'Kygo': [
		'kygo',
		'kyrre',
		'firestone'
	],
	'Kanye West': [
		'kanyewest',
		'kanye',
		'sitdownkanye',
		'kanyeomariwest',
		'yeezus',
	],
	'Justin Timberlake': [
		'justintimberlake',
		'jt202tour',
		'jt',
		'timberbiel',
		'2020experience',
		'jtimberlake',
		'timberlake',
		'jtpresidentofpop',
	],
	'Justin Bieber': [
		'justinbieber',
		'bieber',
		'justinbieberupdates',
		'jb',
		'beliebers',
		'bieberfamily',
		'belieber'
	],
	'Walmart': [
		'walmart',
		'wal-mart'
	],
	'Nike': [
		'nike',
		'freerun2',
		'flyknit',
		'superfly',
	],
	'Test': [
		'follow',
		'kca',
		'ipad',
		'android',
		'retweet',
		'followback',
		'win',
		'iphone',
		'nowplaying',
		'news',
	]
}

class Command(BaseCommand):	
	def handle(self, *args, **kwargs):
		start = time()
		tags_start = Tag.objects.all().count()
		cases_start = Case.objects.all().count()
		for c in CASES:
			self.load(c)
		tags_end = Tag.objects.all().count()
		cases_end = Case.objects.all().count()
		logger.info('Loaded %s tags and %s cases in %s seconds' %(tags_end - tags_start, cases_end - cases_start, round(time() - start, 1)))

	def load(self, c):
		case, created = Case.objects.get_or_create(name=c)
		for t in CASES[c]:
			if not Tag.objects.filter(name__iexact=t).exists():
				tag = Tag.objects.create(name=t)
				case.tags.add(tag)
		case.save()
