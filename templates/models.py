import os

from django.db import models

from .settings import FILEFIELD_PATH


class Template(models.Model):

    path = models.FilePathField(
        path=FILEFIELD_PATH,
        recursive=True)

    class Meta:

        verbose_name = _('Template Link')
        verbose_name_plural = _('Links to Templates for Content Views/Widgets/Pages')
        ordering = ('path',)

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        '''
        Remove the FILEFIELD_PATH and return the template name
        that will be useful for Django template loaders

        FILEFIELD_PATH
        >>> 'templates/'
        self.path
        >>> 'templates/widget/widget_default.html'
        self.name
        >>> 'widget/widget_default.html'
        '''
        if self.path.split(os.sep)[0] in FILEFIELD_PATH:
            return '/'.join(self.path.split(os.sep)[1:])
        return self.path
