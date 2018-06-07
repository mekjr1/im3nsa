# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 07:23
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    INDEX_SQL = """
CREATE INDEX channels_channellog_channel_created_on
ON channels_channellog(channel_id, created_on desc);

CREATE INDEX channels_channelevent_api_view
ON channels_channelevent(org_id, created_on DESC, id DESC)
WHERE is_active = TRUE;

CREATE INDEX channels_channelevent_calls_view
ON channels_channelevent(org_id, "time" DESC)
WHERE is_active = TRUE AND event_type IN ('mt_call', 'mt_miss', 'mo_call', 'mo_miss');
    """

    dependencies = [
        ('channels', '0054_install_triggers'),
    ]

    operations = [
        migrations.RunSQL(INDEX_SQL)
    ]
