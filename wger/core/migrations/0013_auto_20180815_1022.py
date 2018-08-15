# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-15 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='can_create_user',
            field=models.BooleanField(default=False, help_text='Allow user to create users via REST API'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='creator',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='token',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True),
        ),
    ]