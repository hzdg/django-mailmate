from django.contrib import admin
from django.conf import settings
from .models import Email, User
from django.db import connection
from templates import ConfigurableEmail


def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()


def register(cls):

    table = Email.objects.model._meta.db_table

    if db_table_exists(table):
        if(issubclass(cls, ConfigurableEmail)):

            storage, created = Email.objects.get_or_create(
                email_name=cls.__name__
            )

            if created:
                storage.from_email = cls.from_email
                storage.subject = cls.subject
                storage.save()

        else:
            raise Exception("class should inherit from ConfigurableEmail")
    else:
        pass


class UserAdmin(admin.ModelAdmin):
    pass


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email_name', 'subject', 'from_email')


"""Add to admin if DJANGO_MAILMATE_ADMIN is true in settings file"""

try:
    setting = settings.DJANGO_MAILMATE_ADMIN
    if setting is True:
        admin.site.register(Email, EmailAdmin)
        admin.site.register(User, UserAdmin)
except:
    pass
