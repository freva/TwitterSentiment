# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_auto_20150225_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='text',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
    ]
