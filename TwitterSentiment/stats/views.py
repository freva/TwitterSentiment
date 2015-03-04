from django.shortcuts import render
from .models import CaseStats, TagStats
from TwitterSentiment.scraper.models import Case, Tag

def cases(request):
	cases = []
	for c in Case.objects.all():
		cases.append(CaseStats.objects.filter(case=c).last())
	return render(request, 'cases.html',
		{'cases':cases})

def hashtags(request):
	hashtags = []
	for t in Tag.objects.all():
		hashtags.append(TagStats.objects.filter(tag=t).last())
	return render(request, 'hashtags.html',
		{'hashtags':hashtags})