Setup
---------------------------

``pip install django-mailmate``

How-To
-----------------------------

In emails.py ::


        from mailmate.templates import TemplatedEmailMessage

        class CoolMessage(TemplatedEmailMessage):
            to = ['some-user@some-email.com']
            from_email = 'no-reply@some-email.com'
            subject = 'Super Cool Message'
            template_name = 'emails/text-template.txt'
            html_template_name = 'emails/html-template.html'


In views.py ::


        from .emails import CoolMessage
        CoolMessage(extra_context={'user': 'You', 'is': 'Cool'}).send()
