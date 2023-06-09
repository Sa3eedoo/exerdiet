# Generated by Django 4.2.1 on 2023-06-09 21:23

import core.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('category', models.CharField(choices=[('F', 'Food'), ('B', 'Beverage'), ('S', 'Seasoning')], default='F', max_length=1)),
                ('calories', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('carbs', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(0)])),
                ('fats', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(0)])),
                ('protein', models.DecimalField(decimal_places=1, max_digits=4, validators=[django.core.validators.MinValueValidator(0)])),
                ('image', models.ImageField(blank=True, null=True, upload_to='diet/images/foods', validators=[core.validators.validate_image_size])),
            ],
        ),
        migrations.CreateModel(
            name='Water',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('drinking_date', models.DateField()),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='waters', to='core.trainee')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('instructions', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='diet/images/recipes', validators=[core.validators.validate_image_size])),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='core.trainee')),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('time_eaten', models.DateTimeField(auto_now_add=True)),
                ('recipes', models.ManyToManyField(blank=True, related_name='meals', to='diet.recipe')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='core.trainee')),
            ],
        ),
        migrations.CreateModel(
            name='FoodInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=1, max_digits=5, validators=[django.core.validators.MinValueValidator(1)])),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_instances', to='diet.food')),
                ('meal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='food_instances', to='diet.meal')),
                ('recipe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='food_instances', to='diet.recipe')),
            ],
            options={
                'verbose_name': 'Food Instance',
                'verbose_name_plural': 'Food Instances',
                'db_table': 'diet_food_instance',
            },
        ),
        migrations.CreateModel(
            name='CustomFood',
            fields=[
                ('food_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='diet.food')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_foods', to='core.trainee')),
            ],
            options={
                'verbose_name': 'Custom Food',
                'verbose_name_plural': 'Custom Foods',
                'db_table': 'diet_custom_food',
            },
            bases=('diet.food',),
        ),
    ]
