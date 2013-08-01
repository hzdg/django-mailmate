from mailmate import TemplatedEmailMessage
from mailmate.exceptions import MissingBody
import pytest


def test_body_required():
    """
    You must define either a body or a template.
    """
    with pytest.raises(MissingBody):
        TemplatedEmailMessage().message()


def test_empty_body():
    """
    If you explicitly set the body to an empty string, a MissingBody error
    shouldn't be raised.
    """
    TemplatedEmailMessage(body='').message()


def test_body_template():
    """
    The body string can be a template.
    """
    email = TemplatedEmailMessage(body='hello {{ name }}',
                                  extra_context={'name': 'world'})
    assert email.body == 'hello world'


def test_subject_template():
    """
    The subject can be a template.
    """
    email = TemplatedEmailMessage(subject='hello {{ name }}',
                                  body='',
                                  extra_context={'name': 'world'})
    assert email.message()['Subject'] == 'hello world'


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


def test_autoplaintext():
    email = TemplatedEmailMessage(html_template_name='simple_body.html')
    assert email.body.strip() == 'hello world'
