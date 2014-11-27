# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0004_auto_20141127_0638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='name',
        ),
    ]
