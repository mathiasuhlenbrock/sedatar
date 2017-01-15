import csv
from subprocess import call
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Update the app's ASCII tables.
        # ------------------------------

        # Update sedatar/data/csv/databases.csv.
        # Not automated.
        # Update sedatar/data/csv/news.csv.
        # Not automated.

        # Update astronomical_database/data/csv/catalogues.csv.
        # Not automated.
        # Update astronomical_database/data/csv/categories.csv.
        # Not automated.
        # Update astronomical_database/data/csv/planets.csv.
        call(["astronomical_database/scripts/shell/update_planets_csv.sh"])

        # Update the rdf database.
        # ------------------------

        # Update astronomical_database/data/rdf/astronomical_database.rdf.
        execfile("astronomical_database/scripts/python/update_rdf.py")
