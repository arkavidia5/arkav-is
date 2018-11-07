from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User, RegistrationConfirmationAttempt, PasswordResetConfirmationAttempt


def resend_email(modeladmin, request, queryset):
    for obj in queryset:
        obj.send_email()


resend_email.short_description = 'Resend the confirmation email of the selected attempts with the same token.'


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no username field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'is_staff', 'is_active', 'is_email_confirmed')
    search_fields = ('email', 'full_name')
    ordering = ('email',)


@admin.register(RegistrationConfirmationAttempt)
class RegistrationConfirmationAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_confirmed', 'email_last_sent_at']
    list_filter = ['is_confirmed']
    search_fields = ['user']
    readonly_fields = ['user', 'token', 'email_last_sent_at']
    actions = [resend_email]

    class Meta:
        ordering = ['-email_last_sent_at']


@admin.register(PasswordResetConfirmationAttempt)
class PasswordResetConfirmationAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_confirmed', 'email_last_sent_at']
    list_filter = ['is_confirmed']
    search_fields = ['user']
    readonly_fields = ['user', 'token', 'email_last_sent_at']
    actions = [resend_email]

    class Meta:
        ordering = ['-email_last_sent_at']
