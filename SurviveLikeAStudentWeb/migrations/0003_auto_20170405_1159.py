# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-05 04:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SurviveLikeAStudentWeb', '0002_profile_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
