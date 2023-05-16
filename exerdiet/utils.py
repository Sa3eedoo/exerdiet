import random
from faker import Faker
from datetime import datetime, timedelta
from django.utils import timezone
from passlib.hash import pbkdf2_sha256
import pytz

from core.models import User, Trainee


fake = Faker()

activity_levels = [choice[0] for choice in Trainee.ActivityLevel.choices]
goals = [choice[0] for choice in Trainee.Goal.choices]
genders = [choice[0] for choice in Trainee.Gender.choices]

def get_fake_users(count=10):
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        password = fake.password()
        encrypted_password = pbkdf2_sha256.hash(password)
        
        data = {
            "username": profile.get('username'),
            "email": profile.get('mail'),
            "password": encrypted_password,
            "is_active": False,
            "date_joined": timezone.make_aware(fake.date_time_this_decade(), timezone=pytz.UTC),
            "is_superuser": fake.boolean(),
            "is_staff": fake.boolean(),
            # "last_login": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        }
        
        if 'name' in profile:
            fname, lname = profile.get('name').split(" ")[:2]
            data['first_name'] = fname
            data['last_name'] = lname
        user_data.append(data)
    return user_data


def get_fake_trainees(count=10):
    trainees_data = []
    for _ in range(count):
        existing_users = User.objects.filter(trainee__isnull=True, is_superuser=False)
        users_count = existing_users.count()
        
        if users_count > 0:
            fake_user = existing_users[0]
        else:
            fake_users = get_fake_users(1)
            fake_user = User.objects.create(**fake_users[0])
            
        trainee = Trainee()
        trainee.user = fake_user
        trainee.birthdate = fake.date_of_birth(minimum_age=18, maximum_age=100)
        trainee.gender = random.choice(genders)
        trainee.height = round(random.uniform(150, 200), 1)
        trainee.weight = round(random.uniform(50, 100), 1)
        trainee.activity_level = random.choice(activity_levels)
        trainee.goal = random.choice(goals)
        trainee.carbs_ratio = trainee.get_default_macronutrients_ratios()[0]
        trainee.fats_ratio = trainee.get_default_macronutrients_ratios()[1]
        trainee.protein_ratio = trainee.get_default_macronutrients_ratios()[2]
        
        trainee.daily_calories_needs = trainee.calculate_daily_calories_needs()
        trainee.daily_water_needs = trainee.calculate_daily_water_needs()
        
        trainee.save()  # Save the trainee object to the database

        trainees_data.append(trainee)
    return trainees_data

