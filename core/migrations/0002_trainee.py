# Generated by Django 4.1.7 on 2023-03-05 23:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField()),
                ('height', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(400)])),
                ('weight', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(800)])),
                ('calories_needs', models.PositiveIntegerField()),
                ('calories_intake', models.PositiveIntegerField()),
                ('calories_burned', models.PositiveIntegerField()),
                ('water_intake', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('water_needs', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('carbs_ratio', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('fats_ratio', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('protein_ratio', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('was_active_today', models.BooleanField()),
                ('streak', models.PositiveIntegerField()),
                ('activity_level', models.CharField(choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')], default='M', max_length=1)),
                ('goal', models.CharField(choices=[('G', 'Gain'), ('K', 'Keep'), ('L', 'Lose')], default='K', max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
