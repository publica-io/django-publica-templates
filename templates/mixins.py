from django.db import models
from django.template import Context
from django.template.loader import get_template



class TemplateMixin(models.Model):
    template_name_suffix = '_detail'
    preview_template_name_suffix = '_preview'

    template = models.ForeignKey(
        'templates.Template',
        related_name='%(app_label)s_%(class)s_templates',
        null=True,
        blank=True
    )
    preview_template = models.ForeignKey(
        'templates.Template',
        related_name='%(app_label)s_%(class)s_preview_templates',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


    def _render(self, template_suffix, context=None):

        if self.template.name:
            template_name = self.template.name
        else:
            template_name = '{}/{}{}.html'.format(
                self._meta.app_label,
                self._meta.model_name,
                template_suffix
            )
    
        if context is None:
            context = {}
    
        context[self.__class__.__name__.lower()] = self

        template = get_template(template_name)

        return template.render(context)

    def render(self, context=None):
        return self._render(self.template_name_suffix, context)


    def render_preview(self, context=None):
        return self._render(self.preview_template_name_suffix, context)
