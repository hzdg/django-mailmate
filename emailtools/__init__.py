from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from version import __version__


class BaseTemplatedEmailMessage(EmailMultiAlternatives):
    """
    """
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
            connection=None, attachments=None, headers=None, alternatives=None,
            cc=None, template=None, html_template=None, extra_context=None):

        subject = self._get_value('subject', subject)
        body = self._get_value('body', body)
        from_email = self._get_value('from_email', from_email)
        to = self._get_value('to', to)
        bcc = self._get_value('bcc', bcc)
        connection = self._get_value('connection', connection)
        attachments = self._get_value('attachments', attachments)
        headers = self._get_value('headers', headers)
        alternatives = self._get_value('alternatives', alternatives)
        cc = self._get_value('cc', cc)
        kwargs = {}
        if cc:
            kwargs['cc'] = cc

        self.template = self._get_value('template', template)
        self.html_template = self._get_value('html_template', html_template)
        self.extra_context = self._get_value('extra_context', extra_context)

        super(BaseTemplatedEmailMessage, self).__init__(subject=subject, 
                    body=body,from_email=from_email, to=to, bcc=bcc, 
                    connection=connection,  attachments=attachments, 
                    headers=headers, alternatives=alternatives, **kwargs)

    def get_templates(self, *args, **kwargs):
        """
        Returns a list of "standard template" names. Must return a list.
        """
        if self.template is None:
            raise ImproperlyConfigured(
                "TemplatedEmailMessage requires either a definition of "
                "'template' or an implementation of 'get_templates()'")
        else:
            return [self.template]

    def get_html_templates(self, *args, **kwargs):
        """
        Returns a list of "alternative template" names. Must return a list.
        """
        if self.html_template is None:
            raise ImproperlyConfigured(
                "TemplatedEmailMessage requires either a definition of "
                "'html_template' or an implementation of 'get_html_templates()'")
        else:
            return [self.html_template]

    def get_context_data(self, **kwargs):
        context_data = self.extra_context.copy() if self.extra_context else {}
        context_data.update(kwargs)
        return context_data

    def get_context(self, context_dict={}):
        return Context(self.get_context_data(**context_dict))

    def send(self, fail_silently=False):
        self.body = self._render_template()
        if self.html_template:
            self.attach_alternative(self._render_html_template(), 'text/html')

        return super(BaseTemplatedEmailMessage, self).send(fail_silently)

    def _render_template(self):
        """
        Renders standard template with context
        """
        template = loader.get_template(self.get_templates()[0])
        return template.render(self.get_context())

    def _render_html_template(self):
        """
        Renders alternative template with context
        """
        template = loader.get_template(self.get_html_templates()[0])
        return template.render(self.get_context())
    
    def _get_value(self, attr, value):
        return value or getattr(self.__class__, attr, None) or value
        
        


class TemplatedEmailMessage(BaseTemplatedEmailMessage):
    """
    example:
    class MyMessage(TemplatedEmailMessage):
        to = ['chrismc@hzdg.com']
        from_email = 'chrismc@hzdg.com'
        template = 'emails/referral.html'
        html_template = 'emails/referral-html.html'

    my_message = MyMessage(extra_context={'name': 'Chris McKenzie'})
    """
    pass
