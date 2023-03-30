from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from . import models


class TraineeStatusFilter(admin.SimpleListFilter):
    title = 'trainee status'
    parameter_name = 'is_trainee__exact'

    FILTER_TRUE = '1'
    FILTER_FALSE = '0'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_TRUE, 'Yes'),
            (self.FILTER_FALSE, 'No')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_TRUE:
            return queryset.filter(trainee__isnull=False)
        if self.value() == self.FILTER_FALSE:
            return queryset.filter(trainee__isnull=True)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    actions = ['activate_users', 'deactivate_users',
               'staff_users', 'destaff_users',
               'spuer_users', 'despuer_users']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
    list_display = ["username", "email", "first_name",
                    "last_name", "is_staff", 'trainee_status']
    list_filter = ("is_staff", "is_superuser", "is_active",
                   "groups", TraineeStatusFilter)
    list_per_page = 100
    search_fields = ['username__istartswith', 'first_name__istartswith',
                     'last_name__istartswith', 'email']

    @admin.display(ordering='trainee')
    def trainee_status(self, user):
        if user.trainee:
            url = (
                reverse('admin:core_trainee_changelist') +
                str(user.trainee.id)
            )
            return format_html('<a href="{}">{}</a>', url, True)
        return False

    @admin.action(description='Activate selected users')
    def activate_users(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        message = f'{updated_count} users were activated.'
        self.message_user(request, message)

    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        message = f'{updated_count} users were deactivated.'
        self.message_user(request, message)

    @admin.action(description='Make selected users staff members')
    def staff_users(self, request, queryset):
        updated_count = queryset.update(is_staff=True)
        message = f'{updated_count} users joined staff.'
        self.message_user(request, message)

    @admin.action(description='Make selected users Not staff members')
    def destaff_users(self, request, queryset):
        updated_count = queryset.update(is_staff=False)
        message = f'{updated_count} users left staff.'
        self.message_user(request, message)

    @admin.action(description='Make selected users super users')
    def spuer_users(self, request, queryset):
        updated_count = queryset.update(is_superuser=True)
        message = f'{updated_count} users are now super users.'
        self.message_user(request, message)

    @admin.action(description='Make selected users Not super users')
    def despuer_users(self, request, queryset):
        updated_count = queryset.update(is_superuser=False)
        message = f'{updated_count} users are no longer super users.'
        self.message_user(request, message)


@admin.register(models.Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_select_related = ['user']
    search_fields = ['user__username__istartswith', 'user__first_name__istartswith',
                     'user__last_name__istartswith', 'user__email']
