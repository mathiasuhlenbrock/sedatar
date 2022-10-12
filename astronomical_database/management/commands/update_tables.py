from subprocess import call
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        call(['astronomical_database/scripts/shell/update_planets_csv.sh'])
