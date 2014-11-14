#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-publica-templates
------------

Tests for `django-publica-templates` models module.
"""


import unittest

from templates import models
from django.template import loader, Context, TemplateDoesNotExist
from django.core.management import call_command
from django.conf import settings as django_settings

# from templates.conf import settings
import test_settings as settings
from templates.utils.cache import get_cache_key
from templates.utils.template import check_template_syntax



class TemplatesTestCase(unittest.TestCase):
    def setUp(self):
        self.old_template_loaders = settings.TEMPLATE_LOADERS
        if 'templates.loader.Loader' not in settings.TEMPLATE_LOADERS:
            loader.template_source_loaders = None
            settings.TEMPLATE_LOADERS = (list(settings.TEMPLATE_LOADERS) +
                                         ['templates.loader.Loader'])

        self.t1, _ = models.Template.objects.get_or_create(
            name='base.html', content='base')
        self.t2, _ = models.Template.objects.get_or_create(
            name='sub.html', content='sub')

    def tearDown(self):
        loader.template_source_loaders = None
        settings.TEMPLATE_LOADERS = self.old_template_loaders

    def test_basiscs(self):
        self.assertTrue("base" in self.t1.content)

    def test_load_templates(self):
        result = loader.get_template("templates/test.html").render(Context({}))
        self.assertEqual(result, 'test')

    def test_check_template_syntax(self):
        bad_template, _ = models.Template.objects.get_or_create(
            name='bad.html', content='{% if foo %}Bar')
        good_template, _ = models.Template.objects.get_or_create(
            name='good.html', content='{% if foo %}Bar{% endif %}')
        self.assertFalse(check_template_syntax(bad_template)[0])
        self.assertTrue(check_template_syntax(good_template)[0])

    def test_get_cache_name(self):
        self.assertEqual(get_cache_key('name with spaces'),
                         'templates::name-with-spaces')