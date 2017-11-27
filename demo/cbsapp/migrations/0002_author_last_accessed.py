# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cbsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='last_accessed',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 27, 9, 42, 10, 856000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
