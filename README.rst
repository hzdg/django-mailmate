Setup
---------------------------

``pip install -e git+git@github.com:hzdg/django-emailtools.git#egg=django-emailtools``

How-To
-----------------------------

In emails.py ::

    
        from emailtools.templates import TemplatedEmailMessage
    
        class CoolMessage(TemplatedEmailMessage):
            to = ['some-user@some-email.com']
            from_email = 'no-reply@some-email.com'
            subject = 'Super Cool Message'
            template_name = 'emails/text-template.txt'
            html_template_name = 'emails/html-template.html'


In views.py ::

    
        from .emails import CoolMessage
        CoolMessage(extra_context={'user': 'You', 'is': 'Cool'}).send()
