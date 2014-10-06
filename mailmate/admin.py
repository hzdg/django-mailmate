from django.contrib import admin
from .models import Email, User


class UserAdmin(admin.ModelAdmin):
    pass


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email_name', 'subject', 'from_email')


admin.site.register(Email, EmailAdmin)
admin.site.register(User, UserAdmin)
