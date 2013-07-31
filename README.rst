Setup
---------------------------

``pip install django-mailmate``


How-To
-----------------------------

In myapp.emails.py::

    from mailmate.templates import TemplatedEmailMessage

    class MyEmail(TemplatedEmailMessage):
        to = ['some-user@some-email.com']
        from_email = 'no-reply@some-email.com'
        subject = 'Hello, {{ name }}!'
        body = 'Your position is: {{ position }}'

Elsewhere::

    from myapp.emails import MyEmail
    email = MyEmail(extra_context={'name': 'Christopher', 'position': 100})
    email.send()

You can also use separate template files for your email bodies::

    class MyEmail(TemplatedEmailMessage):
        to = ['some-user@some-email.com']
        from_email = 'no-reply@some-email.com'
        subject = 'Hello, {{ name }}!'
        template_name = 'emails/my_email.txt'

\...and easily specify an HTML template::

    class MyEmail(TemplatedEmailMessage):
        to = ['some-user@some-email.com']
        from_email = 'no-reply@some-email.com'
        subject = 'Hello, {{ name }}!'
        template_name = 'emails/my_email.txt'
        html_template_name = 'emails/my_email.html'
