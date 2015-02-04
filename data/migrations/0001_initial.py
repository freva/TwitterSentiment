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
                ('created_at', models.DateTimeField()),
                ('subjectivity', models.DecimalField(max_digits=5, decimal_places=3)),
                ('polarity', models.DecimalField(max_digits=5, decimal_places=3)),
                ('x', models.DecimalField(max_digits=18, decimal_places=15)),
                ('y', models.DecimalField(max_digits=18, decimal_places=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
