from django.core.management.base import BaseCommand
from freight_app.models import User

class Command(BaseCommand):
    help = 'Seeds the database with an initial admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@freightflowlogistics.com', 'admin123', role='admin')
            self.stdout.write(self.style.SUCCESS('Successfully created initial admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists. Skipping.'))
