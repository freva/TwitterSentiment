from django.contrib import admin
from .models import *

class TweetAdmin(admin.ModelAdmin):
	list_display = ('hashtag', 'city', 'state', 'polarity')
	list_filter = ('hashtag',)

class CaseAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at',)
	search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'created_at')
	search_fields = ('name',)

admin.site.register(Tweet, TweetAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Tag, TagAdmin)
