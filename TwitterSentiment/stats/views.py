from django.shortcuts import render
from .models import CaseStats, TagStats
from TwitterSentiment.scraper.models import Case, Tag
from time import time

def cases(request):
	return render(request, 'cases.html',
		{'cases':CaseStats.objects.filter(active=True)})

def hashtags(request):
	return render(request, 'hashtags.html',
		{'hashtags':TagStats.objects.filter(active=True)})