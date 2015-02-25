from TwitterSentiment.scraper.management.commands import load_cases
from django_ajax.decorators import ajax
from django.shortcuts import render
from TwitterSentiment.scraper.models import Tweet
import json
from django.http import HttpResponse
from .aggregate_tweets import JsonConverter


def home(request):
    return render(request, 'base.html')


@ajax
def get_hashtag(request):
    cases = load_cases.CASES
    rawSearch, hashtags = [term.lower() for term in request.POST.get('hashtag').split(",")], []

    for searchTerm in rawSearch:
        if "#" in searchTerm:
            hashtags.append(searchTerm[1:])
        elif searchTerm in cases:
            hashtags.extend(cases[searchTerm])

    results = JsonConverter.searchHashtags(hashtags)
    return {'results': results}


@ajax
def get_suggestions(request):
    cases, results = load_cases.CASES, []

    for label in cases.keys():
        if label.index(request) == 0 or label.index(" " + request) > 0:
            results.append({"case": label, "name": label})

    for label in cases.keys():
        for hashtag in cases[label]:
            if hashtag.index(request) == 0 or hashtag.index(" " + request) > 0:
                results.append({"case": label, "name": "#" + hashtag})
    return results