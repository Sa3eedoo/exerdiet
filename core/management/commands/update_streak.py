from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Trainee


class Command(BaseCommand):
    help = 'Updates streak of all trainees'

    def handle(self, *args, **options):
        print('updating streak of all trainees...')
        with transaction.atomic():
            for trainee in Trainee.objects.all():
                if trainee.was_active_today:
                    trainee.daily_streak += 1
                    trainee.was_active_today = False
                else:
                    trainee.daily_streak = 0
                trainee.save()
