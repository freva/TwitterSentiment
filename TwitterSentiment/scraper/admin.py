from django.contrib import admin
from .models import *

class TweetAdmin(admin.ModelAdmin):
	list_display = ('hashtag', 'city', 'state', 'polarity')
	list_filter = ('hashtag',)

admin.site.register(Tweet, TweetAdmin)
