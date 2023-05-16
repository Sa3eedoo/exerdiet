from django.core.management.base import BaseCommand
from core.models import Trainee

from ratings.models import Rating
from ratings.tasks import generate_fake_reviews


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
        parser.add_argument("--trainees", default=1000, type=int)
        parser.add_argument("--show-total", action='store_true', default=False)
    
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        trainee_count = options.get('trainees')
        # print(count, show_total, trainee_count)
        new_ratings = generate_fake_reviews(count=count, trainees=trainee_count)
        print(f"New ratings: {len(new_ratings)}")
        if show_total:
            qs = Rating.objects.all()
            print(f"Total ratings: {qs.count()}")