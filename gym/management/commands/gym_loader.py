from django.core.management.base import BaseCommand
from gym import utils as gym_utils
from gym.models import Exercise, Workout, ExerciseInstance

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
        parser.add_argument("--show-total", action='store_true', default=False)
        parser.add_argument("--create-exercises", action='store_true', default=False)
        parser.add_argument("--create-workouts", action='store_true', default=False)
        
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        create_exercises = options.get('create_exercises')
        create_workouts = options.get('create_workouts')
    
        if create_exercises:
            fake_exercises = gym_utils.get_fake_exercises(count=count)
            new_exercises = [Exercise(**fake_exercise) for fake_exercise in fake_exercises]
            exercise_bulk = Exercise.objects.bulk_create(new_exercises, ignore_conflicts=True)
            print(f"New exercises: {len(exercise_bulk)}")
            
        if create_workouts:
            fake_workouts = gym_utils.get_fake_workouts(count=count)
            new_workouts = []

            for fake_workout in fake_workouts:
                exercises_data = fake_workout.pop('exercises')  # Remove exercises from the workout data
                workout = Workout.objects.create(**fake_workout)  # Create the workout

                for exercise_data in exercises_data:
                    exercise_instance = ExerciseInstance.objects.create(workout=workout, **exercise_data)
                    workout.exercise_instances.add(exercise_instance)

                new_workouts.append(workout)

            print(f"New workouts: {len(new_workouts)}")
        
        if show_total:
            if create_exercises:
                print(f"Total exercises: {Exercise.objects.count()}")
            if create_workouts:
                print(f"Total workouts: {Workout.objects.count()}")