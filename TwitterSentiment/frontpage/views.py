from TwitterSentiment.scraper.management.commands import load_cases
from TwitterSentiment.frontpage.graph_tweets import graphHashtags
from django_ajax.decorators import ajax
from django.shortcuts import render
from TwitterSentiment.scraper.models import Tweet, Tag, Case
import json
import datetime
from django.http import HttpResponse
from .aggregate_tweets import JsonConverter

def home(request):
    searchTerms = [{"case": label, "name": label, "id": ','.join(load_cases.CASES[label])}
                   for label in load_cases.CASES.keys()]

    searchTerms += [{"case": label, "name": "#" + hashtag, "id": hashtag}
                    for label in load_cases.CASES.keys() for hashtag in load_cases.CASES[label]]

    return render(request, 'base.html',
        {'tags': json.dumps(searchTerms)})


@ajax
def get_hashtag(request):
    hashtags = list(set(request.POST.get('hashtag').split(",")))
    startTime = datetime.datetime.strptime(request.POST.get('startTime'), "%d/%m/%Y %H:%M")
    endTime = datetime.datetime.strptime(request.POST.get('endTime'), "%d/%m/%Y %H:%M")

    results = JsonConverter.searchHashtags(hashtags, startTime, endTime)
    return {'results': results}

@ajax
def get_tokens(request):
    out = [{"name": label, "id": ','.join(load_cases.CASES[label])} for label in load_cases.CASES.keys()]
    out += [{"name": "#" + hashtag, "id": hashtag}
                    for label in load_cases.CASES.keys() for hashtag in load_cases.CASES[label]]
    return out


@ajax
def graph_hashtag(request):
    hashtags = list(set(request.POST.get('hashtag').split(",")))
    startTime = datetime.datetime.strptime(request.POST.get('startTime'), "%d/%m/%Y %H:%M")
    endTime = datetime.datetime.strptime(request.POST.get('endTime'), "%d/%m/%Y %H:%M")

    return graphHashtags(hashtags, startTime, endTime)