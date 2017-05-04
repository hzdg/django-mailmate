from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context, loader
from .exceptions import MissingBody


ALLOWED_TAGS = ['a', 'b', 'i', 'strong', 'em', 'hr', 'blockquote', 'br', 'ol',
                'ul', 'li', 'p', 'img'] + ['h%s' % n for n in range(1, 7)]


class TemplatedEmailMessage(EmailMultiAlternatives):
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

    def __init__(self, subject='', body=None, from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, alternatives=None,
                 cc=None, template_name=None, html_template_name=None,
                 extra_context=None):

        self.subject_template = self._get_value('subject', subject)
        self.body_template = self._get_value('body', body)
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

        alternatives = alternatives or []
        html_body = self.render_html_body()
        if html_body is not None:
            alternatives.append((html_body, 'text/html'))

        super(TemplatedEmailMessage, self).__init__(
            subject=self.render_subject(),
            body=self.render_body(), from_email=from_email, to=to, bcc=bcc,
            connection=connection, attachments=attachments,
            headers=headers, alternatives=alternatives, **kwargs)

    def get_context_data(self):
        return self.extra_context.copy() if self.extra_context else {}

    def get_context(self):
        return Context(self.get_context_data())

    def render_body(self):
        """
        Renders standard template with context
        """
        if self.body_template is not None:
            body = Template(self.body_template).render(self.get_context())
        elif self.template_name is not None:
            body = loader.get_template(self.template_name).render(self.get_context())
        else:
            try:
                body = self.body
            except AttributeError:
                body = None
            try:
                from markdownify import markdownify
            except ImportError:
                pass
            else:
                html_body = self.render_html_body()
                if html_body is not None:
                    body = markdownify(html_body, convert=ALLOWED_TAGS)
            if body is None:
                raise MissingBody('The email does not have a body. Either'
                                  ' provide a body or template_name or, if you'
                                  ' really want to send an email without a'
                                  ' body, set the body to an empty string'
                                  ' explicitly.')
        return body

    def render_subject(self):
        return Template(self.subject_template).render(self.get_context())

    def render_html_body(self):
        """
        Renders alternative template with context
        """
        if self.html_template_name:
            template = loader.get_template(self.html_template_name)
            return template.render(self.get_context())

    def _get_value(self, attr, value):
        return value or getattr(self.__class__, attr, None) or value
