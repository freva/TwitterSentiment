from django.shortcuts import render
from .models import CaseStats, TagStats

def cases(request):
	return render(request, 'cases.html',
		{'cases':CaseStats.objects.all()})

def hashtags(request):
	return render(request, 'hashtags.html',
		{'hashtags':TagStats.objects.all()})