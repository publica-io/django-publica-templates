# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text="Example: 'flatpages/default.html'", max_length=1024, verbose_name='name')),
                ('content', models.TextField(verbose_name='content', blank=True)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation date')),
                ('last_changed', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last changed')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'template',
                'verbose_name_plural': 'templates',
            },
            bases=(models.Model,),
        ),
    ]
