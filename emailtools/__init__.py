from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader


__version__ = (0, 1, 0)


class BaseTemplatedEmailMessage(EmailMultiAlternatives):
    """
    """
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
            connection=None, attachments=None, headers=None, alternatives=None,
            cc=None, standard_template=None, alternative_template=None):
        
        self.standard_template = standard_template
        self.alternative_template = alternative_template
        
        # TODO: should user pass in mime type as seperate property or a tuple with the 
        # alternative_template path and mimetype ?


    def get_standard_templates(self, *args, **kwargs):
        """
        Returns a list of "standard template" names. Must return a list.
        """
        return [ self.standard_template ]
        if self.standard_template is None:
            raise ImproperlyConfigured(
                "TemplatedEmailMessage requires either a definition of "
                "'standard_template' or an implementation of 'get_standard_templates()'")
        else:
            return [self.standard_template]

    def get_alternative_templates(self, *args, **kwargs):
        """
        Returns a list of "alternative template" names. Must return a list.
        """
        return [ self.alternative_template ]
        if self.alternative_template is None:
            raise ImproperlyConfigured(
                "TemplatedEmailMessage requires either a definition of "
                "'alternative_template' or an implementation of 'get_alternative_templates()'")
        else:
            return [self.alternative_template]

    def get_context_data(self, context_dict):
        return context_dict

    def get_context(self, context_dict = {}):
        return Context(self.get_context_data(context_dict))


    def _render_standard_template(self):
        """
        Renders standard template with context
        """
        template = loader.get_template(self.get_standard_templates()[0])
        return template.render(self.get_context())

    def _render_alternative_template(self):
        """
        Renders alternative template with context
        """
        template = loader.get_template(self.get_alternative_templates()[0])
        return template.render(self.get_context())    
    
    
    def send(self, fail_silently=False):
        
        if self.alternative_template:
            self.attach_alternative(self._render_alternative_template())
        
        return super(TemplatedEmailMessage, self).send(fail_silently)
        
        


class TemplatedEmailMessage(BaseTemplatedEmailMessage):
    pass


# class EmailFormGenerator(EmailGenerator):
# 
#     context_overrides = {}
#     
#     def __init__(self, form_instance, **kwargs):
#         super(EmailFormGenerator, self).__init__(**kwargs)
#         self.form = form_instance
#         
#     def _get_context_from_form(self):
#         if not self.form.is_valid():
#             raise Exception("")
#         return self.form.cleaned_data
#         
#     
#     def get_context_data(self, context_dict):
#         context_dict = super(EmailFormGenerator, self).get_context_data(context_dict)
#         form_context = self._get_context_from_form()
#         context_dict.update(form_context)
#         context_dict['all_fields'] = copy.deepcopy(form_context)
#         context_dict.update(self.context_overrides)
#         return context_dict


# class MyMessage(EmailGenerator):
#     subject = 'Hey Dudes'
#     template = 'a/b/c.txt'
#     html_template = 'a/b/c.html'
