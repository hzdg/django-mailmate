from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader


class BaseTemplatedEmailMessage(EmailMultiAlternatives):
    """
    """

    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, alternatives=None,
                 cc=None, template_name=None, html_template_name=None,
                 extra_context=None):

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

        self.template_name = self._get_value('template_name', template_name)
        self.html_template_name = self._get_value('html_template_name',
                                                  html_template_name)
        self.extra_context = self._get_value('extra_context', extra_context)

        super(BaseTemplatedEmailMessage, self).__init__(
            subject=subject,
            body=body, from_email=from_email, to=to, bcc=bcc,
            connection=connection, attachments=attachments,
            headers=headers, alternatives=alternatives, **kwargs)

    def get_template_names(self, *args, **kwargs):
        """
        Returns a list of "standard template" names. Must return a list.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplatedEmailMessage requires either a definition of "
                "'template' or an implementation of 'get_templates()'")
        else:
            return [self.template_name]

    def get_html_template_names(self, *args, **kwargs):
        """
        Returns a list of "alternative template" names. Must return a list.
        """
        if self.html_template_name is not None:
            return [self.html_template_name]
        return None

    def get_context_data(self, **kwargs):
        context_data = self.extra_context.copy() if self.extra_context else {}
        context_data.update(kwargs)
        return context_data

    def get_context(self, context_dict={}):
        return Context(self.get_context_data(**context_dict))

    def send(self, fail_silently=False):
        self.body = self._render_template()
        if self.get_html_template_names():
            self.attach_alternative(self._render_html_template(), 'text/html')

        return super(BaseTemplatedEmailMessage, self).send(fail_silently)

    def _render_template(self):
        """
        Renders standard template with context
        """
        template = loader.get_template(self.get_template_names()[0])
        return template.render(self.get_context())

    def _render_html_template(self):
        """
        Renders alternative template with context
        """
        template = loader.get_template(self.get_html_template_names()[0])
        return template.render(self.get_context())

    def _get_value(self, attr, value):
        return value or getattr(self.__class__, attr, None) or value


class TemplatedEmailMessage(BaseTemplatedEmailMessage):
    """
    example:
    In Emails.py

        from mailmate import TemplateMessage

        class CoolMessage(TemplateMessage):
            to = ['some-user@some-email.com']
            from_email = 'no-reply@some-email.com'
            subject = 'Super Cool Message'
            template_name = 'emails/text-template.txt'
            html_template_name = 'emails/html-template.html'

    In Views.py

        from .emails import CoolMessage

        message = CoolMessage(extra_context={'user': 'You', 'is': 'Cool'})
        message.send()
    """
    pass
