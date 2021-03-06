#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-publica-templates
------------

Tests for `django-publica-templates` models module.
"""


import unittest

from templates import models
from django.template import loader, Context

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


class TemplateMixins(unittest.TestCase):
    def setUp(self):
        self.old_template_loaders = settings.TEMPLATE_LOADERS
        if 'templates.loader.Loader' not in settings.TEMPLATE_LOADERS:
            loader.template_source_loaders = None
            settings.TEMPLATE_LOADERS = (list(settings.TEMPLATE_LOADERS) +
                                         ['templates.loader.Loader'])

        self.t1, _ = models.Template.objects.get_or_create(
            name='templates/test.html', content='detail')
        self.t2, _ = models.Template.objects.get_or_create(
            name='templates/test.html', content='preview')

        self.temp = models.Templateable()

    def tearDown(self):
        loader.template_source_loaders = None
        settings.TEMPLATE_LOADERS = self.old_template_loaders

    def test_basics(self):
        self.temp.template = self.t1
        self.assertTrue("test" in self.temp.render())

    def test_load_templates_render(self):
        # Set the tempalte t1 as template name and then load seperately and
        # see render works
        self.temp.template = self.t1
        result = loader.get_template("templates/test.html").render(Context({}))
        self.assertEqual(result, self.temp.render())

    def test_load_templates_render_preview(self):
        # Set the tempalte t1 as template name and then load seperately and
        # see render works
        self.temp.preview_template = self.t2
        result = loader.get_template("templates/test.html").render(Context({}))
        self.assertEqual(result, self.temp.render_preview())
