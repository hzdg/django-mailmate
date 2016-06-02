from django.contrib import admin
from django.conf import settings
from .models import Email, User


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
