from typing import Any
from django.contrib import admin
from django.db.models import Count
from django.http import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from . import models


CALORIE_BURNED_LEVEL_LOW = 100
CALORIE_BURNED_LEVEL_HIGH = 250


class CalorieBurnedLevelFilter(admin.SimpleListFilter):
    title = 'calorie burned level'
    parameter_name = 'calorie_burned_level'
    FILTER_ZERO = '0'
    FILTER_LOW = f'<{CALORIE_BURNED_LEVEL_LOW}'
    FILTER_MED = f'<{CALORIE_BURNED_LEVEL_HIGH}'
    FILTER_HIGH = f'>{CALORIE_BURNED_LEVEL_HIGH}'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_ZERO, 'Zero'),
            (self.FILTER_LOW, 'Low'),
            (self.FILTER_MED, 'Medium'),
            (self.FILTER_HIGH, 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_ZERO:
            return queryset.filter(calories_burned=0)
        if self.value() == self.FILTER_LOW:
            return queryset.filter(calories_burned__gt=0).filter(calories_burned__lt=CALORIE_BURNED_LEVEL_LOW)
        if self.value() == self.FILTER_MED:
            return queryset.filter(calories_burned__gte=CALORIE_BURNED_LEVEL_LOW).filter(calories_burned__lt=CALORIE_BURNED_LEVEL_HIGH)
        if self.value() == self.FILTER_HIGH:
            return queryset.filter(calories_burned__gte=CALORIE_BURNED_LEVEL_HIGH)


class CustomExerciseFilter(admin.SimpleListFilter):
    title = 'is custom exercise'
    parameter_name = 'is_custom_exercise'
    FILTER_CUSTOM = '1'
    FILTER_NOT_CUSTOM = '0'

    def lookups(self, request, model_admin):
        return [
            (self.FILTER_CUSTOM, 'Custom Exercises'),
            (self.FILTER_NOT_CUSTOM, 'Not Custom Exercises')
        ]

    def queryset(self, request, queryset):
        if self.value() == self.FILTER_CUSTOM:
            return queryset.filter(customexercise__isnull=False)
        if self.value() == self.FILTER_NOT_CUSTOM:
            return queryset.exclude(customexercise__isnull=False)


@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories_burned_level', 'calories_burned',
                    'is_repetitive', 'body_part']
    list_editable = ['calories_burned', 'is_repetitive', 'body_part']
    list_filter = [CustomExerciseFilter, 'is_repetitive',
                   'body_part', CalorieBurnedLevelFilter]
    list_per_page = 100
    ordering = ['name']
    readonly_fields = ['thumbnail']
    search_fields = ['name']

    class Media:
        css = {
            'all': ['core/styles.css']
        }

    def thumbnail(self, exercise: models.Exercise):
        if exercise.image.name != '':
            return format_html(f'<img src="{exercise.image.url}" class="thumbnail"/>')
        return ''

    @admin.display(ordering='calories_burned')
    def calories_burned_level(self, exercise):
        if exercise.calories_burned == 0:
            return 'Zero'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_LOW:
            return 'Low'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_HIGH:
            return 'Medium'
        return 'High'

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['calories_burned'].widget.attrs['placeholder'] = '1m|10rep'

        return form


@admin.register(models.CustomExercise)
class CustomExerciseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    list_display = ['name', 'trainee_username', 'calories_burned_level', 'calories_burned',
                    'is_repetitive', 'body_part']
    list_filter = ['body_part', 'is_repetitive', CalorieBurnedLevelFilter]
    list_select_related = ['trainee__user']
    list_per_page = 100
    ordering = ['name']
    readonly_fields = ['thumbnail']
    search_fields = ['name', 'trainee__user__username__istartswith']

    class Media:
        css = {
            'all': ['core/styles.css']
        }

    def thumbnail(self, custom_exercise: models.CustomExercise):
        if custom_exercise.image.name != '':
            return format_html(f'<img src="{custom_exercise.image.url}" class="thumbnail"/>')
        return ''

    @admin.display(ordering='trainee__user__username')
    def trainee_username(self, custom_exercise):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(custom_exercise.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, custom_exercise.trainee)

    @admin.display(ordering='calories_burned')
    def calories_burned_level(self, exercise):
        if exercise.calories_burned == 0:
            return 'Zero'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_LOW:
            return 'Low'
        elif exercise.calories_burned < CALORIE_BURNED_LEVEL_HIGH:
            return 'Medium'
        return 'High'

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['calories_burned'].widget.attrs['placeholder'] = '1m|10rep'

        return form


class ExerciseInstanceWorkoutInline(admin.TabularInline):
    model = models.ExerciseInstance
    autocomplete_fields = ['exercise']
    exclude = ['performed_workout']
    extra = 1
    fields = ['exercise', 'duration', 'sets']

    def formfield_for_dbfield(self, db_field, request: HttpRequest | None, **kwargs: Any):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'duration':
            field.widget.attrs['placeholder'] = 'sec|reps'
        return field


@admin.register(models.Workout)
class WorkoutAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    list_display = ['name', 'trainee_username', 'performed_count']
    list_select_related = ['trainee__user']
    list_per_page = 100
    ordering = ['name']
    readonly_fields = ['thumbnail']
    search_fields = ['name', 'trainee__user__username__istartswith']
    inlines = [ExerciseInstanceWorkoutInline]

    class Media:
        css = {
            'all': ['core/styles.css']
        }

    def thumbnail(self, workout: models.Workout):
        if workout.image.name != '':
            return format_html(f'<img src="{workout.image.url}" class="thumbnail"/>')
        return ''

    @admin.display(ordering='trainee__user__username')
    def trainee_username(self, workout):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(workout.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, workout.trainee)

    @admin.display(ordering='performed_count')
    def performed_count(self, workout):
        return workout.performed_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(performed_count=Count('performed_workouts'))


class ExerciseInstancePerformedWorkoutInline(admin.TabularInline):
    model = models.ExerciseInstance
    autocomplete_fields = ['exercise']
    exclude = ['workout']
    extra = 1
    fields = ['exercise', 'duration', 'sets']

    def formfield_for_dbfield(self, db_field, request: HttpRequest | None, **kwargs: Any):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'duration':
            field.widget.attrs['placeholder'] = 'sec|reps'
        return field


class WorkoutPerformedWorkoutInline(admin.TabularInline):
    model = models.Workout.performed_workouts.through
    autocomplete_fields = ['workout']
    extra = 1
    verbose_name = "Workout"
    verbose_name_plural = "Workouts"


@admin.register(models.PerformedWorkout)
class PerformedWorkoutAdmin(admin.ModelAdmin):
    autocomplete_fields = ['trainee']
    exclude = ['workouts']
    list_display = ['name', 'trainee_username', 'time_performed']
    list_filter = ['time_performed']
    list_per_page = 100
    list_select_related = ['trainee__user']
    inlines = [WorkoutPerformedWorkoutInline,
               ExerciseInstancePerformedWorkoutInline]
    ordering = ['time_performed']
    search_fields = ['name', 'trainee__user__username__istartswith']

    @admin.display(ordering='trainee__user__username')
    def trainee_username(self, workout):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(workout.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, workout.trainee)
