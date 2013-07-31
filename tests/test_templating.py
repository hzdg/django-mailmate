from mailmate import TemplatedEmailMessage


def test_optional_template():
    """
    If a body is included, you shouldn't need to define template.
    """
    class Email(TemplatedEmailMessage):
        body = 'hello world'

    Email().message()


def test_template():
    class Email(TemplatedEmailMessage):
        template_name = 'body.txt'

    assert Email(extra_context={'name': 'world'}).body.strip() == 'hello world'


def test_html_template():
    class Email(TemplatedEmailMessage):
        template_name = 'body.txt'
        html_template_name = 'body.html'

    email = Email(extra_context={'name': 'world'})
    assert '<p>hello world</p>' in email.message().as_string()
