import csv
import pytz
import random
from faker import Faker
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from pprint import pprint
from decimal import Decimal
from core.models import User, Trainee
from django.db import IntegrityError


FOOD_CSV = settings.DATA_DIR / "nutrition.csv"
# DATA_DIR = settings.BASE_DIR / "data"

def convert_to_decimal(string_value):
    try:
        numeric_part = string_value.strip("g")  # Remove the "g" unit
        decimal_value = Decimal(numeric_part)
        return decimal_value
    except Exception as e:
        print(f"Error converting string to decimal: {e}")
        return None

def load_food_data(limit=1):
    with open(FOOD_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            _id = row.get("id")
            try:
                _id = int(_id)
            except:
                _id = None
            data = {
                "id": _id,
                "name": row.get('name'),
                "category": 'F',
                "calories": convert_to_decimal(row.get('calories')),
                "carbs": convert_to_decimal(row.get("carbohydrate")),
                "fats": convert_to_decimal(row.get("fat")),
                "protein": convert_to_decimal(row.get("protein")),
            }
            dataset.append(data)
            if i +2 > limit:
                break
        return dataset

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
            "is_superuser": False,
            "is_staff": False,
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
        # existing_users = User.objects.filter(trainee__isnull=True, is_staff=False, is_superuser=False)
        # users_count = existing_users.count()
        
        # if users_count > 0:
        #     fake_user = existing_users[0]
        # else:
        fake_users = get_fake_users(1)
        # fake_user = User.objects.create(**fake_users[0])
        
        try:
            fake_user = User.objects.create(**fake_users[0])
            success_count += 1
        except IntegrityError:
            error_count += 1
            continue
            
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

