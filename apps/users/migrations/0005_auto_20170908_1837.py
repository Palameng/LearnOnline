# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-08 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20170723_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(max_length='100', upload_to='courses/%Y/%m', verbose_name='头像'),
        ),
    ]