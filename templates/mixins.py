from django.db import models
from django.template import Context
from django.template.loader import get_template


class TemplateMixin(object):

    template_name_suffix = '_detail'
    preview_template_name_suffix = '_preview'

    template = models.ForeignKey('templates.Template')
    preview_template = models.ForeignKey('templates.Template')

    def render(self):
        '''
        The method will render if db template is present or else just use default template and render
        '''
        template = get_template(self.template.name if self.template.name else "%s/%s%s.html" % (
            self._meta.app_label,
            self._meta.model_name,
            self.template_name_suffix))
        return template.render(Context({'display': self}))

    def render_preview(self):
        '''
        The method will render if db template is present or else just use default template and render
        '''
        template = get_template(self.preview_template.name if self.preview_template.name else "%s/%s%s.html" % (
            self._meta.app_label,
            self._meta.model_name,
            self.preview_template_name_suffix))
        return template.render(Context({'display': self}))