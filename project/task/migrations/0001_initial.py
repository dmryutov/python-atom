# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-24 10:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('estimate', models.DateTimeField()),
                ('is_done', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
