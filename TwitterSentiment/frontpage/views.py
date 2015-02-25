from TwitterSentiment.scraper.management.commands import load_cases
from django_ajax.decorators import ajax
from django.shortcuts import render
from TwitterSentiment.scraper.models import Tweet
import json
from django.http import HttpResponse
from .aggregate_tweets import JsonConverter


def home(request):
    searchTerms = [{"case": label, "name": label} for label in load_cases.CASES.keys()]
    searchTerms += [{"case": label, "name": "#" + hashtag} for label in load_cases.CASES.keys() for hashtag in load_cases.CASES[label]]

    return render(request, 'base.html',
        {'tags': json.dumps(searchTerms)})


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
