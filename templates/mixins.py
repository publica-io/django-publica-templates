from django.db import models
from django.template import Context
from django.template.loader import get_template


class TemplateMixin(models.Model):

    template_name_suffix = '_detail'
    preview_template_name_suffix = '_preview'

    template = models.ForeignKey(
        'templates.Template', 
        related_name='%(app_label)s_%(class)s_templates'
    )
    preview_template = models.ForeignKey(
        'templates.Template', 
        related_name='%(app_label)s_%(class)s_preview_templates'
    )

    class Meta:
        abstract = True

    def render(self):
        '''
        The method will render if db template is present or else just use default template and render
        '''
        template = get_template(self.template.name if self.template.name else "%s/%s%s.html" % (
            self._meta.app_label,
            self._meta.model_name,
            self.template_name_suffix))
        return template.render(Context({'view': self}))

    def render_preview(self):
        '''
        The method will render if db template is present or else just use default template and render
        '''
        template = get_template(self.preview_template.name if self.preview_template.name else "%s/%s%s.html" % (
            self._meta.app_label,
            self._meta.model_name,
            self.preview_template_name_suffix))
        return template.render(Context({'view': self}))
