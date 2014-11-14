from django.db import models
from django.db.models import signals
from django.template import TemplateDoesNotExist
from django.utils.translation import ugettext_lazy as _

import settings
from utils.cache import add_template_to_cache, remove_cached_template
from utils.template import get_template_source

try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now


class Template(models.Model):
    """
    Defines a template model for use with the database template loader.
    The field ``name`` is the equivalent to the filename of a static template.
    """
    name = models.CharField(_('name'), max_length=100,
                            help_text=_("Example: 'flatpages/default.html'"))
    content = models.TextField(_('content'), blank=True)
    creation_date = models.DateTimeField(_('creation date'),
                                         default=now)
    last_changed = models.DateTimeField(_('last changed'),
                                        default=now)

    objects = models.Manager()

    class Meta:
        db_table = 'django_template'
        verbose_name = _('template')
        verbose_name_plural = _('templates')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def populate(self, name=None):
        """
        Tries to find a template with the same name and populates
        the content field if found.
        """
        if name is None:
            name = self.name
        try:
            source = get_template_source(name)
            if source:
                self.content = source
        except TemplateDoesNotExist:
            pass

    def save(self, *args, **kwargs):
        self.last_changed = now()
        # If content is empty look for a template with the given name and
        # populate the template instance with its content.
        if getattr(settings, 'TEMPLATES_AUTO_POPULATE_CONTENT', 1) and not self.content:
            self.populate()
        super(Template, self).save(*args, **kwargs)


signals.post_save.connect(add_template_to_cache, sender=Template)
signals.pre_delete.connect(remove_cached_template, sender=Template)