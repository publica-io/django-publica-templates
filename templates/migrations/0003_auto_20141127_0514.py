# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0002_auto_20141127_0059'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'ordering': ('path',), 'verbose_name': 'Template Link', 'verbose_name_plural': 'Links to Templates for Content Views/Widgets/Pages'},
        ),
        migrations.RemoveField(
            model_name='template',
            name='content',
        ),
        migrations.RemoveField(
            model_name='template',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='template',
            name='last_changed',
        ),
        migrations.RemoveField(
            model_name='template',
            name='name',
        ),
        migrations.AddField(
            model_name='template',
            name='path',
            field=models.FilePathField(default='', path=b'templates/', recursive=True),
            preserve_default=False,
        ),
    ]
