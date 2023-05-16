from .models import Workout


def task_calculate_workout_ratings(all=False, count=None):
    qs = Workout.objects.needs_updating()
    if all:
        qs = Workout.objects.all()
    qs = qs.order_by('rating_last_updated')
    if isinstance(count, int):
        qs = qs[:count]
    for obj in qs:
        obj.calculate_rating(save=True)