from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
    search_fields = ['username__istartswith',
                     'first_name__istartswith', 'last_name__istartswith']


@admin.register(models.Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_select_related = ['user']
    search_fields = ['user__username__istartswith',
                     'user__first_name__istartswith', 'user__last_name__istartswith']
