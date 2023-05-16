from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
from core.models import Trainee, User
from exerdiet import utils as exerdiet_utils

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", nargs='?', default=10, type=int)
        parser.add_argument("--show-total", action='store_true', default=False)
        parser.add_argument("--create-users", action='store_true', default=False)
        parser.add_argument("--create-trainees", action='store_true', default=False)
    
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        create_users = options.get('create_users')
        create_trainees = options.get('create_trainees')
        
        if create_users:
            fake_users = exerdiet_utils.get_fake_users(count=count)
            new_users = [User(**fake_user) for fake_user in fake_users]
            user_bulk = User.objects.bulk_create(new_users, ignore_conflicts=True)
            print(f"New users: {len(user_bulk)}")
        
        if create_trainees:
            fake_trainees = exerdiet_utils.get_fake_trainees(count=count)
            # trainee_bulk = Trainee.objects.bulk_create(fake_trainees, ignore_conflicts=True)
            print(f"New trainees: {len(fake_trainees)}")
        
        if show_total:
            if create_users:
                print(f"Total users: {User.objects.count()}")
            
            if create_trainees:
                print(f"Total trainees: {Trainee.objects.count()}")
