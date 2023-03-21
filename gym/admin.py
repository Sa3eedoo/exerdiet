from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from . import models


@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'calorie_burned_level', 'calories_burned',
                    'is_repetitive', 'body_part']
    list_editable = ['calories_burned', 'is_repetitive', 'body_part']
    list_per_page = 10
    ordering = ['name']
    search_fields = ['name']

    @admin.display(ordering='calories_burned')
    def calorie_burned_level(self, exercise):
        if exercise.calories_burned == 0:
            return 'Zero'
        elif exercise.calories_burned < 100:
            return 'Low'
        elif exercise.calories_burned < 250:
            return 'Medium'
        return 'High'

    def get_queryset(self, request):
        return super().get_queryset(request).exclude(customexercise__isnull=False)


@admin.register(models.CustomExercise)
class CustomExerciseAdmin(admin.ModelAdmin):
    list_display = ['name', 'trainee_user_name']
    list_select_related = ['trainee__user']

    def trainee_user_name(self, custom_exercise):
        url = (
            reverse('admin:core_trainee_changelist') +
            str(custom_exercise.trainee.id)
        )
        return format_html('<a href="{}">{}</a>', url, custom_exercise.trainee)
