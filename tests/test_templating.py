from mailmate import TemplatedEmailMessage


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
