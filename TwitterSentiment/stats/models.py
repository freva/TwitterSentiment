from django.db import models

from TwitterSentiment.scraper.models import Case, Tag

class CaseStats(models.Model):
	case = models.ForeignKey(Case, blank=True, null=True)
	hashtags = models.IntegerField(blank=True, null=True, default=0)
	tweets = models.IntegerField(blank=True, null=True, default=0)
	subjectivity = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3)
	polarity = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3)
	most_used_hashtag = models.CharField(max_length=100, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.case.name

	def toggle(self):
		self.active = not self.active
		self.save()

	class Meta:
		get_latest_by = 'created_at'


class TagStats(models.Model):
	case = models.ForeignKey(Case, blank=True, null=True)
	tag = models.ForeignKey(Tag, blank=True, null=True)
	tweets = models.IntegerField(blank=True, null=True, default=0)
	subjectivity = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3)
	polarity = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=3)		
	created_at = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.tag.name

	def toggle(self):
		self.active = not self.active
		self.save()

	class Meta:
		get_latest_by = 'created_at'