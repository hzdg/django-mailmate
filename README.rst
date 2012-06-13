Setup
---------------------------

``pip install -e git+git@github.com:hzdg/django-emailtools.git#egg=django-emailtools``

How-To
-----------------------------

In Emails.py ::

    
        from emailtools import TemplateMessage
    
        class CoolMessage(TemplateMessage):
            to = ['some-user@some-email.com']
            from_email = 'no-reply@some-email.com'
            subject = 'Super Cool Message'
            template_name = 'emails/text-template.txt'
            html_template_name = 'emails/html-template.html'


In Views.py ::

    
        from .emails import CoolMessage
    
        message = CoolMessage(extra_context={'user': 'You', 'is': 'Cool'})
        message.send()
