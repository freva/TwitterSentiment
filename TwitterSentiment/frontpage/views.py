from django_ajax.decorators import ajax
from django.shortcuts import render
from TwitterSentiment.scraper.models import Tweet
import json
from django.http import HttpResponse
from .JsonConverter import JsonConverter

def home(request):
	return render(request, 'base.html')

@ajax
def get_hashtag(request):
	hashtag = request.POST.get('hashtag')
	results = JsonConverter.searchHashtags(hashtag)
	return {'results': results}