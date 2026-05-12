"""
Management command: seed_voter_roll
Usage:
    python manage.py seed_voter_roll
    python manage.py seed_voter_roll --clear   # clear existing data first

Seeds the VoterRoll with sample test data so developers can test
the registration flow without needing a real election office database.
"""

from django.core.management.base import BaseCommand
from accounts.models import VoterRoll


SAMPLE_VOTERS = [
    {
        'voter_id': 'VID-TEST000001',
        'email': 'rahul.sharma@example.com',
        'mobile_number': '+91 9876543210',
        'full_name': 'Rahul Sharma',
        'village': 'Koramangala',
        'district': 'Bangalore Urban',
        'state': 'Karnataka',
        'nation': 'India',
    },
    {
        'voter_id': 'VID-TEST000002',
        'email': 'priya.nair@example.com',
        'mobile_number': '+91 9876543211',
        'full_name': 'Priya Nair',
        'village': 'Indiranagar',
        'district': 'Bangalore Urban',
        'state': 'Karnataka',
        'nation': 'India',
    },
    {
        'voter_id': 'VID-TEST000003',
        'email': 'amit.patel@example.com',
        'mobile_number': '+91 9876543212',
        'full_name': 'Amit Patel',
        'village': 'Surat Old City',
        'district': 'Surat',
        'state': 'Gujarat',
        'nation': 'India',
    },
    {
        'voter_id': 'VID-TEST000004',
        'email': 'sunita.devi@example.com',
        'mobile_number': '+91 9876543213',
        'full_name': 'Sunita Devi',
        'village': 'Rampur',
        'district': 'Varanasi',
        'state': 'Uttar Pradesh',
        'nation': 'India',
    },
    {
        'voter_id': 'VID-TEST000005',
        'email': 'arjun.reddy@example.com',
        'mobile_number': '+91 9876543214',
        'full_name': 'Arjun Reddy',
        'village': 'Banjara Hills',
        'district': 'Hyderabad',
        'state': 'Telangana',
        'nation': 'India',
    },
    # Add your real test email here so you can test OTP login
    {
        'voter_id': 'VID-MYTEST0001',
        'email': 'canaracollege5@gmail.com',   # Uses the .env email for OTP testing
        'mobile_number': '+91 9999999999',
        'full_name': 'Test Admin User',
        'village': 'Test Village',
        'district': 'Test District',
        'state': 'Karnataka',
        'nation': 'India',
    },
]


class Command(BaseCommand):
    help = 'Seed the VoterRoll with sample test data for development.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing VoterRoll entries before seeding.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count, _ = VoterRoll.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Cleared {count} existing VoterRoll entries.'))

        created = 0
        skipped = 0

        for voter in SAMPLE_VOTERS:
            obj, was_created = VoterRoll.objects.get_or_create(
                voter_id=voter['voter_id'],
                defaults=voter,
            )
            if was_created:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  [ADDED] {obj.full_name} ({obj.voter_id}) - {obj.village}, {obj.state}"
                    )
                )
            else:
                skipped += 1
                self.stdout.write(f"  [EXISTS] {obj.voter_id}")

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! {created} voters added, {skipped} already existed.'
        ))
        self.stdout.write('')
        self.stdout.write('--- Sample credentials to test registration ---')
        self.stdout.write('  Voter ID : VID-MYTEST0001')
        self.stdout.write('  Email    : canaracollege5@gmail.com')
        self.stdout.write('  (OTP will be sent to this email via SMTP)')
