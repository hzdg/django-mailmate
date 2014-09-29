from django.contrib import admin
from .models import Email, Receiver


class ReceiverInlineAdmin(admin.TabularInline):
    model = Receiver


class EmailAdmin(admin.ModelAdmin):
    inlines = (ReceiverInlineAdmin, )
    list_display = ('email_name', 'subject', 'from_email')


admin.site.register(Email, EmailAdmin)
