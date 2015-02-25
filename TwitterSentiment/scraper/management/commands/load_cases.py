from django.core.management.base import BaseCommand, CommandError
from TwitterSentiment.scraper.models import *

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
		Tag.objects.all().delete()
		Case.objects.all().delete()
		for c in CASES:
			self.load(c)

	def load(self, c):
		case = Case.objects.create(name=c)
		for t in CASES[c]:
			tag = Tag.objects.create(name=t)
			case.tags.add(tag)
		case.save()
