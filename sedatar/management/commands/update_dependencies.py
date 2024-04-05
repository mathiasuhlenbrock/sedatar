from subprocess import call
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        call(['sedatar/scripts/shell/update_python_libs.sh'])
