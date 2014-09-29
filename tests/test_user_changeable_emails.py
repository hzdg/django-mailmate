import pytest


@pytest.fixture
def configurable_email(db):
    from mailmate.templates import ConfigurableEmail

    our_email = ConfigurableEmail(
        from_email='no-reply@face.net',
        to=['blah-a@gmail.com', 'blah-b@gmail.com'],
        subject='%s has a reply about this',
        template_name='body.txt',
        html_template_name='body.html',
    )

    return our_email


@pytest.fixture
def AwesomeMessage():
    from mailmate.templates import ConfigurableEmail

    class AwesomeMessage(ConfigurableEmail):
        from_email = 'no-reply@face.net'
        to = ['blah-a@gmail.com', 'blah-b@gmail.com']
        subject = '%s has a reply about this'
        template_name = 'body.txt'
        html_template_name = 'body.html'

    return AwesomeMessage


@pytest.fixture
def UserFriendlyMessage():
    from mailmate.templates import ConfigurableEmail

    class UserFriendlyMessage(ConfigurableEmail):
        from_email = 'no-reply@face.net'
        to = ['blah-a@gmail.com', 'blah-b@gmail.com']
        subject = '%s has a reply about this'
        template_name = 'body.txt'
        html_template_name = 'body.html'
        email_name = 'Super Awesome Message'

    return UserFriendlyMessage


@pytest.mark.django_db
def test_user_friendly_message(UserFriendlyMessage):
    UserFriendlyMessage()

    from mailmate.models import Email
    assert Email.objects.get(email_name='Super Awesome Message')


@pytest.mark.django_db
def test_message_customization(AwesomeMessage):

    message = AwesomeMessage()
    assert message.subject == '%s has a reply about this'
    assert message.storage.receivers.count() == 2

    from mailmate.models import Email
    awesome_message = Email.objects.get(email_name='AwesomeMessage')
    awesome_message.subject = 'It cherged ermegerd'
    awesome_message.save()

    awesome_message.receivers.create(
        address='test@example.com'
    )

    message = AwesomeMessage()
    assert message.subject == 'It cherged ermegerd'
    assert message.storage.receivers.count() == 3
    assert message.to == [
        'blah-a@gmail.com',
        'blah-b@gmail.com',
        'test@example.com'
    ]


def test_reusable_created(configurable_email):
    assert configurable_email.created


def test_email_to_saved(configurable_email):
    assert configurable_email.storage.receivers.count() == 2
    assert configurable_email.to == ['blah-a@gmail.com', 'blah-b@gmail.com']
