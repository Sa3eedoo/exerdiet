from datetime import date
from typing import Any
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ValidationError
from django.urls import reverse
from django.utils.html import format_html
from . import models

CALORIE_LEVEL_LOW = 1800
CALORIE_LEVEL_HIGH = 2200
AGE_TEEN = 12
AGE_ADULT = 20
AGE_OLD = 60


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
                    "last_name", "is_staff", 'is_active']
    list_filter = ("is_staff", "is_superuser", "is_active",
                   "groups", TraineeStatusFilter)
    list_per_page = 100
    list_select_related = ['trainee']
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


class CalorieLevelFilter(admin.SimpleListFilter):
    title = 'calorie level'
    parameter_name = 'calorie_level'
    FILTER_LOW = f'<{CALORIE_LEVEL_LOW}'
    FILTER_MED = f'<{CALORIE_LEVEL_HIGH}'
    FILTER_HIGH = f'>{CALORIE_LEVEL_HIGH}'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_LOW, 'Low'),
            (self.FILTER_MED, 'Medium'),
            (self.FILTER_HIGH, 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_LOW:
            return queryset.filter(daily_calories_needs__gt=0).filter(daily_calories_needs__lt=CALORIE_LEVEL_LOW)
        if self.value() == self.FILTER_MED:
            return queryset.filter(daily_calories_needs__gte=CALORIE_LEVEL_LOW).filter(daily_calories_needs__lt=CALORIE_LEVEL_HIGH)
        if self.value() == self.FILTER_HIGH:
            return queryset.filter(daily_calories_needs__gte=CALORIE_LEVEL_HIGH)


class AgeFilter(admin.SimpleListFilter):
    title = 'age'
    parameter_name = 'age'
    FILTER_LOW = f'>{AGE_TEEN}'
    FILTER_MED = f'>{AGE_ADULT}'
    FILTER_HIGH = f'>{AGE_OLD}'

    today = date.today()

    teen_min_birthdate = date(
        today.year - AGE_ADULT, today.month, today.day
    )
    teen_max_birthdate = date(today.year - AGE_TEEN, today.month, today.day)

    adult_min_birthdate = date(
        today.year - AGE_OLD + 1, today.month, today.day
    )
    adult_max_birthdate = date(today.year - AGE_ADULT, today.month, today.day)

    old_min_birthdate = date(today.year - AGE_OLD, today.month, today.day)

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_LOW, 'Teen'),
            (self.FILTER_MED, 'Adult'),
            (self.FILTER_HIGH, 'Old')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_LOW:
            return queryset.filter(birthdate__range=(self.teen_min_birthdate, self.teen_max_birthdate))
        if self.value() == self.FILTER_MED:
            return queryset.filter(birthdate__range=(self.adult_min_birthdate, self.adult_max_birthdate))
        if self.value() == self.FILTER_HIGH:
            return queryset.filter(birthdate__lt=self.old_min_birthdate)


class TraineeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Trainee
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        carbs_ratio = cleaned_data.get('carbs_ratio')
        fats_ratio = cleaned_data.get('fats_ratio')
        protein_ratio = cleaned_data.get('protein_ratio')

        if cleaned_data.get('is_macronutrients_ratios_custom'):
            if carbs_ratio and fats_ratio and protein_ratio:
                if ((carbs_ratio + fats_ratio + protein_ratio) != 1.0):
                    raise ValidationError(
                        'Macronutrients(carbs, fats, protein) ratios are not valid.'
                    )
        return cleaned_data


@admin.register(models.Trainee)
class TraineeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    exclude = ['was_active_today']
    actions = ['make_active', 'make_inactive', 'clear_streak']
    form = TraineeAdminForm
    list_display = ['name', 'username', 'age', 'gender', 'height', 'weight',
                    'calorie_level', 'activity_level', 'goal', 'was_active_today', 'streak',]
    list_filter = [CalorieLevelFilter, AgeFilter,
                   'activity_level', 'goal', 'was_active_today']
    list_select_related = ['user']
    list_per_page = 100
    ordering = ['user__first_name', 'user__last_name']
    readonly_fields = ['thumbnail']
    search_fields = ['user__username__istartswith', 'user__first_name__istartswith',
                     'user__last_name__istartswith', 'user__email']

    class Media:
        css = {
            'all': ['core/styles.css']
        }

    def thumbnail(self, trainee: models.Trainee):
        if trainee.image.name != '':
            return format_html(f'<img src="{trainee.image.url}" class="thumbnail"/>')
        return ''

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['daily_calories_needs'].initial = None
        form.base_fields['daily_water_needs'].initial = None
        form.base_fields['carbs_ratio'].initial = None
        form.base_fields['fats_ratio'].initial = None
        form.base_fields['protein_ratio'].initial = None
        form.base_fields['daily_streak'].initial = None

        form.base_fields['birthdate'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
        form.base_fields['height'].widget.attrs['placeholder'] = 'in cm'
        form.base_fields['weight'].widget.attrs['placeholder'] = 'in kg'
        form.base_fields['daily_calories_needs'].widget.attrs['placeholder'] = 'leave it'
        form.base_fields['daily_water_needs'].widget.attrs['placeholder'] = 'leave it'
        form.base_fields['carbs_ratio'].widget.attrs['placeholder'] = 'leave blank to be calculated'
        form.base_fields['fats_ratio'].widget.attrs['placeholder'] = 'leave blank to be calculated'
        form.base_fields['protein_ratio'].widget.attrs['placeholder'] = 'leave blank to be calculated'

        return form

    @admin.display(ordering='birthdate')
    def name(self, trainee):
        return trainee.full_name()

    @admin.display(ordering='user__username')
    def username(self, trainee):
        url = (
            reverse('admin:core_user_changelist') +
            str(trainee.user.id)
        )
        return format_html('<a href="{}">{}</a>', url, trainee)

    @admin.display(ordering='birthdate')
    def age(self, trainee):
        return trainee.age()

    @admin.display(ordering='daily_calories_needs')
    def calories_needs(self, trainee):
        return trainee.daily_calories_needs

    @admin.display(ordering='daily_calories_needs')
    def calorie_level(self, trainee):
        if trainee.daily_calories_needs < CALORIE_LEVEL_LOW:
            return 'Low'
        elif trainee.daily_calories_needs < CALORIE_LEVEL_HIGH:
            return 'Medium'
        return 'High'

    @admin.display(ordering='daily_streak')
    def streak(self, trainee):
        return trainee.daily_streak

    @admin.action(description='Make selected trainees active')
    def make_active(self, request, queryset):
        updated_count = queryset.update(was_active_today=True)
        message = f'{updated_count} trainees were made active.'
        self.message_user(request, message)

    @admin.action(description='Make selected trainees inactive')
    def make_inactive(self, request, queryset):
        updated_count = queryset.update(was_active_today=False)
        message = f'{updated_count} trainees were made inactive.'
        self.message_user(request, message)

    @admin.action(description='Clear streak of selected trainees')
    def clear_streak(self, request, queryset):
        updated_count = queryset.update(daily_streak=0)
        message = f'{updated_count} trainees` streaks were cleared.'
        self.message_user(request, message)
