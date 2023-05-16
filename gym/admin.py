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
    list_display = ['id', 'name', 'calories_burned_level', 'calories_burned',
                    'is_repetitive', 'body_part']
    list_editable = ['calories_burned', 'is_repetitive', 'body_part']
    list_filter = [CustomExerciseFilter, 'is_repetitive',
                   'body_part', CalorieBurnedLevelFilter]
    list_per_page = 100
    ordering = ['name']
    search_fields = ['name']

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
    list_display = ['id', 'name', 'trainee_username', 'calories_burned_level', 'calories_burned',
                    'is_repetitive', 'body_part']
    list_filter = ['body_part', 'is_repetitive', CalorieBurnedLevelFilter]
    list_select_related = ['trainee__user']
    list_per_page = 100
    ordering = ['name']
    search_fields = ['name', 'trainee__user__username__istartswith']

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


@admin.register(models.ExerciseInstance)
class ExerciseInstanceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['exercise', 'workout', 'performed_workout']
    list_display = ['id', 'exercise_name', 'duration', 'sets',
                    'workout_name', 'performed_workout_name']
    list_display_links = ['duration', 'sets']
    list_per_page = 100
    list_select_related = [
        'exercise', 'workout__trainee__user', 'performed_workout__trainee__user'
    ]
    ordering = ['exercise__name']
    search_fields = ['food__name', 'workouts__name',
                     'performed_workout__trainee__user__username__istartswith']

    @admin.display(ordering='exercise__name')
    def exercise_name(self, exercise_instacne):
        url = (
            reverse('admin:gym_exercise_changelist') +
            str(exercise_instacne.exercise.id)
        )
        return format_html('<a href="{}">{}</a>', url, exercise_instacne.exercise)

    @admin.display(ordering='workout__name')
    def workout_name(self, exercise_instacne):
        if exercise_instacne.workout:
            url = (
                reverse('admin:gym_workout_changelist') +
                str(exercise_instacne.workout.id)
            )
            return format_html('<a href="{}">{}</a>', url, exercise_instacne.workout)
        return exercise_instacne.workout

    @admin.display(ordering='performed_workout_name')
    def performed_workout_name(self, exercise_instacne):
        if exercise_instacne.performed_workout:
            url = (
                reverse('admin:gym_performedworkout_changelist') +
                str(exercise_instacne.performed_workout.id)
            )
            return format_html('<a href="{}">{}</a>', url, exercise_instacne.performed_workout)
        return exercise_instacne.performed_workout

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields['duration'].widget.attrs['placeholder'] = 'sec|reps'

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
    list_display = ['id', 'name', 'trainee_username', 'performed_count', 'is_public', 'calculate_ratings_count']
    readonly_fields = ['calculate_ratings_count']
    list_select_related = ['trainee__user']
    list_per_page = 100
    ordering = ['name']
    search_fields = ['name', 'trainee__user__username__istartswith']
    inlines = [ExerciseInstanceWorkoutInline]

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
    list_display = ['id', 'name', 'trainee_username', 'time_performed']
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
