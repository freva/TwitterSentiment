from TwitterSentiment.scraper.management.commands import load_cases
from django_ajax.decorators import ajax
from django.shortcuts import render
from TwitterSentiment.scraper.models import Tweet, Tag, Case
import json
from django.http import HttpResponse
from .aggregate_tweets import JsonConverter
from .stats import Cases, Hashtags


def home(request):
    searchTerms = [{"case": label, "name": label, "id": ','.join(load_cases.CASES[label])}
                   for label in load_cases.CASES.keys()]

    searchTerms += [{"case": label, "name": "#" + hashtag, "id": hashtag}
                    for label in load_cases.CASES.keys() for hashtag in load_cases.CASES[label]]

    return render(request, 'base.html',
        {'tags': json.dumps(searchTerms)})

def cases(request):
	cases = [Cases(c) for c in Case.objects.all().order_by('name')]
	hashtags_from_cases = sum([c.hashtags for c in cases])
	tweets_from_cases = sum([c.tweets for c in cases])
	return render(request, 'cases.html',
		{'cases':[Cases(c) for c in Case.objects.all().order_by('name')],
		'hashtags_from_cases':hashtags_from_cases,
		'tweets_from_cases':tweets_from_cases,
		'hashtags_from_database':Tag.objects.count(),
		'tweets_from_database':Tweet.objects.count()})

def hashtags(request):
	hashtags = [Hashtags(t) for t in Tag.objects.all().order_by('name')]
	tags = len(hashtags)
	tweets = sum([h.tweets for h in hashtags])
	return render(request, 'hashtags.html',
		{'hashtags':hashtags,
		'tags':tags,
		'tweets':tweets})

@ajax
def get_hashtag(request):
    hashtags = list(set(request.POST.get('hashtag').split(",")))

    results = JsonConverter.searchHashtags(hashtags)
    return {'results': results}
