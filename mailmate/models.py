"""
    Colin Wood, 09/26/14

    Use the email model to create a new email with mixing in the
    TemplatedEmailMessage response class.

    .. code-block:: python

        from mailmate.templates import ConfigurableEmail

        class CoolEmail(ConfigurableEmail):
            from_email = 'no-reply@my-company.com
            to = ['default-one@company.com', 'default-two@company.com']
            template_name = 'emails/super-awesome-email.txt'
            html_template_name = 'emails/super-awesome-email.html'

        message = CoolEmail(extra_context=data_dict)
        message.send()

    Once this is done it will initialize a new email in the admin. Allowing
    a admin user to change out values for from, to, subject, etc to be what
    they want. If nothing is setup it will just used the programmed
    defaults.

    By default nothing is changeable but will show up as a registered email
    message and essentially the same as you just doing a TemplatedEmailMessage.
    The difference is when intiailized with a new email its defaults will be
    fetched from the DB rather than through the attribute getters.

"""
from django.db import models
from .strings import (
    IS_TESTING_HELP_TEXT,
    IS_TEST_USER_HELP_TEXT,
    IS_ENABLED_HELP_TEXT
)


class Receiver(models.Model):
    address = models.EmailField()
    is_test_user = models.BooleanField(default=False,
                                       help_text=IS_TEST_USER_HELP_TEXT)


class Email(models.Model):

    email_name = models.CharField(max_length=100)
    from_email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200, blank=True)
    is_enabled = models.BooleanField(default=True,
                                     help_text=IS_ENABLED_HELP_TEXT)

    is_testing = models.BooleanField(default=False,
                                     help_text=IS_TESTING_HELP_TEXT)

    receivers = models.ManyToManyField(Receiver)
