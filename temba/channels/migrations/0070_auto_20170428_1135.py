# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 14:35
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0069_auto_20170427_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='address',
            field=models.CharField(blank=True, help_text='Address with which this channel communicates', max_length=255, null=True, verbose_name='Address'),
        ),
    ]