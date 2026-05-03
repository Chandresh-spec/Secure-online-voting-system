import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a Village Admin interactively or via arguments'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--village', type=str, help='Admin village name')
        parser.add_argument('--district', type=str, help='Admin district name')
        parser.add_argument('--state', type=str, help='Admin state name')

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("--- Create Village Admin ---"))

        username = options.get('username') or input("Enter Username: ")
        email = options.get('email') or input("Enter Email: ")
        password = options.get('password') or input("Enter Password: ")
        
        # Location info
        village = options.get('village') or input("Enter Village Name (e.g. Indiranagar): ")
        district = options.get('district') or input("Enter District (e.g. Bangalore): ")
        state = options.get('state') or input("Enter State (e.g. Karnataka): ")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"User '{username}' already exists!"))
            return

        # Create the user
        admin = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name="Admin",
            last_name=village,
            role="admin",
            village=village,
            district=district,
            state=state,
            is_verified=True,          # Pre-verify admins
            is_staff=True,             # Give Django /admin access
            is_superuser=True          # Complete superuser power
        )

        self.stdout.write(self.style.SUCCESS(f"\n[SUCCESS] Village Admin '{username}' created successfully for '{village}'!"))
        self.stdout.write("You can now log in at http://127.0.0.1:8000/login/ with:")
        self.stdout.write(f"  Email:    {email}")
        self.stdout.write(f"  Password: {password}")
