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
	],
	'Obamacare':[
		"obamacare",
		"obama-care",
		"patientprotectionandaffordablecareact",
		"ppaca",
		"affordablecareact",
		"aca",
		"buynowsavelater",
		"obamahealthcare",
		"staycovered",
		"thisiswhy",
		"readysetenroll",
		"getcovered",
	],
	'Democrats' : [
		"democrat",
		"democrats",
	],
	'Republicans':[
		"republican",
		"republicans",
		"gop",
	],
	'Adidas':[
		"adidas",
		"adidassamba",
		"adidasoriginals",
		"adidasspecial",
		"adidasgazelle",
	],
	'Converse':[
		"converse",
		"convers",
		"jualsepatu",
		"juansepatuconverse",
	],
	'Vans':[
		"vans",
		"vansoriginal",
		"vanscalifornia",
		"vansera59",
		"vansoldskool",
		"vanslove",
		"vanspro",
		"vansclassic",
		"vansaddict",
		"jualsepatuvans",
	],
	'Google':[
		"google",
		"android",
		"galaxys6",
		"galaxys5",
		"galaxys4",
		"galaxys3",
		"galaxys2",
		"galaxys1",
		"samsung",
	],
	'Apple':[
		"iphone",
		"iphone7",
		"iphone6",
		"iphone5",
		"iphone4",
		"iphone3",
		"iphone2",
		"iphone1",
		"max",
		"macbook",
		"macair",
		"stevejobs",
		"ios",
		"ipad",
	],
	'Hund':[
		"dog",
		"dogs",
		"puppy",
	],
	'Katt':[
		"cat",
		"cats",
		"kitten",
	],
	'Christianity':[
		"christ",
		"god",
		"jesus",
		"pray",
		"godbless",
		"bible",
		"christian",
		"catholic",
		"pope",
		"popefrancis",
	],
	'Islam':[
		"allah",
		"quran",
		"mecca",
		'muslim',
		'islam',
		"muhammed",
		"muhammad",
	],
	'Game of Thrones':[
		"gameofthrones",
		"got",
		"gotexhibit",
		"gotcompendium",
		"gotseason5",
		"gotseason4",
		"gotseason3",
		"gotseason2",
		"gotseason1",
		"oberynmartell",
		"winteriscoming",
		"beatifuldeath",
		"maisewilliams",
		"valarmorghulis",
		"allmenmustdie",
		"takethethrone",
		"jonsnow",
		"joffrey",
		"westeros",
		"housebaratheon",
		"targaryen",
		"baratheon",
		"nedstark",
		"lannister",
		"georgerrmartin",
		"thenorth",
		"fucktheking",
		"jeoffrey",
		"stannis",
		"housebolton",
		"roosebolton",
		"joffreybaratheon",
		"tyrell",
		"housetyrell",
		"margaerytyrell",
		"redwedding",
	],
	'Better Call Saul':[
		"bettercallsaul",
		"bcs",
	],
	'House of Cards':[
		"houseofcards",
		"frankunderwood",
		"onenationunderwood",
		"kevinspacey",
	],
	'Community':[
		"community",
	],
	'March Madness':[
		"marchmadness",
	],
	'NHL, kamp Nashville':[
		"preds",
		"smashville",
		"nyr",
		"nshvsnyr",
		"nhl",
	],
	'NHL, kamp Los Angeles':[
		"lackings",
		"nhlducks",
		"9inarow",
		"4inarow",
		"lakvsana",
		"crashville",
		"0inarow",
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
	'Beyonce':[
		"beyonce",
	],
	'Lady Gaga':[
		"ladygaga",
		"gaga",
	],
	'Rihanna':[
		"rihanna",
	],
	'Taylor Swift':[
		"taylorswift",
		"tswift",
	],
	'Nicki Minaj':[
		"nickiminaj",
		"nicki",
		"minaj",
	],
	'Katy Perry':[
		"katyperry",
		"katyp",
	],
	'Ed Sheeran':[
		"edsheeran",
		"sheeran",
	],
	'Chris Brown':[
		"chrisbrown",
	],
	'Kanye West': [
		'kanyewest',
		'kanye',
		'sitdownkanye',
		'kanyeomariwest',
		'yeezus',
		'mbdtf',
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
		"nikeairmax90",
		"nikerunning",
		"nikeairmax1",
		"jordan",
		"jordans",
		"airjordan",
		"airjordan11",
		"justdoit",
		"nikefree",
		"nikepegasus",
		"jualnike",
		"nikewomen",
		"nikemen",
		"nikeplus",
		"jualanike",
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
