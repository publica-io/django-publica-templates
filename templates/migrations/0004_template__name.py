# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0003_auto_20141127_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='_name',
            field=models.CharField(default='', max_length=1024, editable=False),
            preserve_default=False,
        ),
    ]
