from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Tests database connection'

    def handle(self, *args, **options):
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('Database connection successful'))
        except Exception as e:
            self.stdout.write(self.style.ERROR('Database connection error: %s' % e))