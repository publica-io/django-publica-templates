# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_name(apps, schema_editor):
    Template = apps.get_model('templates', 'Template')
    for t in Template.objects.all():
        t.path = t.name
        t.save()


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0003_auto_20141127_0514'),
    ]

    operations = [
        migrations.RunPython(migrate_name)
    ]
