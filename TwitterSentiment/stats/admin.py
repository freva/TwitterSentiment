from django.contrib import admin
from .models import CaseStats, TagStats

class CaseStatsAdmin(admin.ModelAdmin):
	list_display = ('case', 'hashtags', 'tweets', 'subjectivity', 'polarity', 'most_used_hashtag', 'created_at')
	list_filter = ('case',)

class TagStatsAdmin(admin.ModelAdmin):
	list_display = ('case', 'tag', 'tweets', 'subjectivity', 'polarity', 'created_at')
	list_filter = ('case', 'tag',)

admin.site.register(CaseStats, CaseStatsAdmin)
admin.site.register(TagStats, TagStatsAdmin)