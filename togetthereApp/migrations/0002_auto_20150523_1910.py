# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('togetthereApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sp',
            name='elevator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sp',
            name='entrance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sp',
            name='facilities',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sp',
            name='parking',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sp',
            name='toilets',
            field=models.BooleanField(default=False),
        ),
    ]
