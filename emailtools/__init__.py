from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import copy


__version__ = (0, 1, 0)


class EmailGeneratorBase(object):
    """
    Email Processor is a essentially a view for rendering email templates
    and sending them.
    """    
    standard_template = ''
    html_template = ''
    
    to = []
    from_email = ''
    subject = ''
    
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
    
    def get_standard_template(self):
        return self.standard_template
        
    def get_html_template(self):
        return self.html_template
    
    def get_context_data(self, context_dict):
        return context_dict
    
    def get_context(self, context_dict = {}):
        return Context(self.get_context_data(context_dict))

    def _render_standard_template(self):
        template = get_template(self.get_standard_template())
        return template.render(self.get_context())
    
    def _render_html_template(self):
        template = get_template(self.get_html_template())
        return template.render(self.get_context())
    
    def _send(self):
        if not isinstance(self.to, list):
            self.to = [self.to]
            
        msg = EmailMultiAlternatives(self.subject, 
                self._render_standard_template(), self.from_email, self.to)
        if self.get_html_template():
            msg.attach_alternative(self._render_html_template(), "text/html")
        msg.send()
    
    def send(self):
        self._send()


class EmailGenerator(EmailGeneratorBase):
    pass


class EmailFormGenerator(EmailGenerator):

    context_overrides = {}
    
    def __init__(self, form_instance, **kwargs):
        super(EmailFormGenerator, self).__init__(**kwargs)
        self.form = form_instance
        
    def _get_context_from_form(self):
        if self.form.is_valid():
            return self.form.cleaned_data
        return None
    
    def get_context_data(self, context_dict):
        context_dict = super(EmailFormGenerator, self).get_context_data(context_dict)
        form_context = self._get_context_from_form()
        context_dict.update(form_context)
        context_dict['all_fields'] = copy.deepcopy(form_context)
        context_dict.update(self.context_overrides)
        return context_dict
