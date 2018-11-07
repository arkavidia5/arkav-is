from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, EmailConfirmationAttempt, PasswordResetAttempt


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('full_name',)}),
        (_('Permissions'), {'fields': ('email_confirmed' ,'is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('email',)


@admin.register(EmailConfirmationAttempt)
class EmailConfirmationAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'confirmed')


@admin.register(PasswordResetAttempt)
class PasswordResetAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'used')
