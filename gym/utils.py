import random
from faker import Faker

from gym.models import Exercise
from core.models import Trainee

fake = Faker()

body_part = [choice[0] for choice in Exercise.BodyPart.choices]

def get_fake_exercises(count=10):
    exercises_data = []
    for _ in range(count):
        data = {
            "name": fake.word(),
            "body_part": random.choice(body_part),
            "calories_burned": fake.random_int(min=0, max=500),
            'is_repetitive': fake.boolean(),
        }
        exercises_data.append(data)
    return exercises_data
    
    
def get_fake_workouts(count=10):
    workouts_data = []
    trainees = Trainee.objects.all()
    exercises = Exercise.objects.all()
    
    for _ in range(count):
        random_trainee = random.choice(trainees)
        random_exercises = random.sample(list(exercises), k=random.randint(1, 5))
        random_exercises_data = []
        
        
        for exercise in random_exercises:
            duration = fake.random_int(min=10, max=60)
            sets = fake.random_int(min=1, max=5)
            exercise_data = {
                "exercise": exercise,
                "duration": duration,
                "sets": sets,
            }
            random_exercises_data.append(exercise_data)

        data = {
            "name": fake.word(),
            "instructions": fake.paragraphs(nb=3),
            "is_public": True,
            "trainee": random_trainee,
            "exercises": random_exercises_data,
        }
        workouts_data.append(data)
    return workouts_data