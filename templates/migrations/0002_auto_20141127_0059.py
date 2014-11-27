# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='template',
            options={'ordering': ('name',), 'verbose_name': 'Template Link', 'verbose_name_plural': 'Links to Templates for Content Views/Widgets/Pages'},
        ),
    ]
