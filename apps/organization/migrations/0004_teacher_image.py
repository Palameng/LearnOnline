# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-26 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20170822_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teachers/%Y/%m', verbose_name='头像'),
        ),
    ]
