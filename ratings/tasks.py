import random
from core.models import Trainee
from gym.models import Workout
from .models import Rating, RatingChoice


def generate_fake_reviews(count=100, trainees=10, null_avg=False):
    trainee_s = Trainee.objects.first().id # 1
    trainee_e = Trainee.objects.last().id
    random_trainee_ids = random.sample(range(trainee_s, trainee_e), trainees)
    trainees = Trainee.objects.filter(id__in=random_trainee_ids)
    workouts = Workout.objects.all().order_by("?")[:count]
    if null_avg:
        workouts = Workout.objects.filter(rating_avg__isnull=True).order_by("?")[:count]
    n_ratings = workouts.count()
    rating_choices = [x for x in RatingChoice.values if x is not None]
    trainee_ratings = [random.choice(rating_choices) for _ in range(0, n_ratings)]
    
    new_ratings = []
    for workout in workouts:
        rating_obj = Rating.objects.create(
            content_object=workout,
            value=trainee_ratings.pop(),
            trainee=random.choice(trainees)
        )
        new_ratings.append(rating_obj.id)
    return new_ratings