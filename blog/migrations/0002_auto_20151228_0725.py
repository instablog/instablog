# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 07:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='post',
            name='is_public',
        ),
        migrations.RemoveField(
            model_name='post',
            name='lnglat',
        ),
    ]
