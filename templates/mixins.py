from django.db import models
from django.template import Context
from django.template.loader import get_template

try:
    from polymorphic import PolymorphicModel
except ImportError:
    PolymorphicModel = None


class TemplateMixin(models.Model):
    template_name_suffix = '_detail'
    preview_template_name_suffix = '_preview'

    template = models.ForeignKey(
        'templates.Template',
        help_text='Choose a template to render this content',
        related_name='%(app_label)s_%(class)s_templates',
        null=True,
        blank=True
    )

    preview_template = models.ForeignKey(
        'templates.Template',
        verbose_name='Listing/Preview Template',
        help_text='Optionally choose a Listing Template that will be used in List Views',
        related_name='%(app_label)s_%(class)s_preview_templates',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


    def get_template_name(self, template_suffix):

        if self.template:
            template_name = self.template.name
        else:
            template_name = '{}/{}{}.html'.format(
                self._meta.app_label,
                self._meta.model_name,
                template_suffix
            )
        return template_name


    def _render(self, template_suffix, context=None):
    
        if context is None:
            context = {}
    
        # We may be dealing with a Polymorphic Model here
        # so to preserve the reuse of our templates, we want to
        # add the current object under the context key of the
        # base superclass, e.g.:
        # 
        # class WidgetChild(Widget):
        #     #...
        # 
        # will yield 'widget'

        klass_name = self.__class__.__name__.lower()

        if PolymorphicModel is not None:
            # If we have polymorphic models; recurse and try 
            # to discover the base class.
            bases = [b for b in self.__class__.__bases__
                 if issubclass(b, PolymorphicModel)
                 and not b._meta.abstract and not b._meta.proxy]

            if len(bases) == 1:
                klass_name = self.__class__.__bases__[0].__name__.lower()

        context[klass_name] = self

        template = get_template(self.get_template_name(template_suffix))

        return template.render(context)


    def render(self, context=None):
        return self._render(self.template_name_suffix, context)


    def render_preview(self, context=None):
        return self._render(self.preview_template_name_suffix, context)
