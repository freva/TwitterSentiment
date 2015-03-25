from TwitterSentiment.scraper.management.commands import load_cases
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
def search_hashtag(request):
    query = request.GET.get('q', '')

    out = [{"name": label, "id": ','.join(load_cases.CASES[label])} for label in load_cases.CASES.keys() if query in label]
    out += [{"name": "#" + hashtag, "id": hashtag}
                    for label in load_cases.CASES.keys() for hashtag in load_cases.CASES[label] if query in hashtag]
    return out


@ajax
def graph_hashtag(request):
    hashtags = list(set(request.GET.get('hashtag', '').split(",")))
    startTime = datetime.datetime.strptime(request.GET.get('from', ''), "%d/%m/%Y %H:%M")
    endTime = datetime.datetime.strptime(request.GET.get('to', ''), "%d/%m/%Y %H:%M")

    return [hashtags, startTime, endTime]