# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-22 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('slug', models.TextField()),
                ('cover', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='BiblePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.IntegerField()),
                ('image_small', models.ImageField(upload_to='')),
                ('image_large', models.ImageField(blank=True, null=True, upload_to='')),
                ('bible', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bible.Bible')),
            ],
        ),
    ]
