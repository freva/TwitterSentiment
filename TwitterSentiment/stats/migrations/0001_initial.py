# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_auto_20150225_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashtags', models.IntegerField(default=0, null=True, blank=True)),
                ('tweets', models.IntegerField(default=0, null=True, blank=True)),
                ('subjectivity', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('polarity', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('most_used_hashtag', models.CharField(max_length=100, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(blank=True, to='scraper.Case', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweets', models.IntegerField(default=0, null=True, blank=True)),
                ('subjectivity', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('polarity', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(blank=True, to='scraper.Case', null=True)),
                ('tag', models.ForeignKey(blank=True, to='scraper.Tag', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
