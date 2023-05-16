from django.core.management.base import BaseCommand
from core.models import Trainee
from gym.tasks import task_calculate_workout_ratings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=1_000, type=int)
        parser.add_argument("--all", action='store_true', default=False)
    
    def handle(self, *args, **options):
        all = options.get('all')
        count = options.get('count')
        task_calculate_workout_ratings(all=all, count=count)