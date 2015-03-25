# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casestats',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AlterModelOptions(
            name='tagstats',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AddField(
            model_name='casestats',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tagstats',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
