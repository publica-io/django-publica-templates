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

    def render(self, context=None):
        '''
        The method will render if db template is present or else just use
        default template and render

        '''

        if self.template.name:
            template_name = self.template.name
        else:
            template_name = '{}/{}{}.html'.format(
                self._meta.app_label,
                self._meta.model_name,
                self.template_name_suffix
            )

        template = get_template(template_name)
        return template.render(Context({
            'view': self,

            # This should *not* be here, django-compressor is nuts
            'STATIC_URL': '/static/'
        }))

    def render_preview(self, context=True):
        '''
        The method will render if db template is present or else just use
        default template and render

        '''

        if self.preview_template.name:
            template_name = self.preview_template.name
        else:
            template_name = '{}/{}{}.html'.format(
                self._meta.app_label,
                self._meta.model_name,
                self.preview_template_name_suffix
            )
        template_name = template_name
        template = get_template(template_name)
        return template.render(Context({'view': self}))
