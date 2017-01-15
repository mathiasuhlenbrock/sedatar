import csv
from subprocess import call
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Update the database.
        # --------------------
        execfile("sedatar/scripts/python/update.py")
        execfile("astronomical_database/scripts/python/update.py")
