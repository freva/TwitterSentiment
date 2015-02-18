# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', models.CharField(unique=True, max_length=200)),
                ('hashtag', models.CharField(max_length=50, null=True, blank=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('retweet_count', models.IntegerField(default=0, null=True, blank=True)),
                ('favorite_count', models.IntegerField(default=0, null=True, blank=True)),
                ('lat', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('lng', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('state', models.CharField(max_length=3, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('subjectivity', models.DecimalField(null=True, max_digits=5, decimal_places=3, blank=True)),
                ('polarity', models.DecimalField(null=True, max_digits=5, decimal_places=3, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
