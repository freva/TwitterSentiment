from django.shortcuts import render
from TwitterSentiment.scraper.models import Tweet
import json
from django.http import HttpResponse
from .JsonConverter import JsonConverter

def home(request):
	return render(request, 'base.html',
		{'tweets':Tweet.objects.all()})

def get_hashtag(request, hashtag):
	jsonconverter = JsonConverter()
	jsonconverter.set_hashtag(hashtag)
	jsonconverter.run()
	results = jsonconverter.get_dictionary()
	return HttpResponse(json.dumps(results), content_type='application/json')
