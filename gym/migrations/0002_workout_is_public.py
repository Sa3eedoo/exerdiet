# Generated by Django 4.2.1 on 2023-05-15 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
