from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        exec(open('sedatar/scripts/python/update.py').read())
        exec(open('astronomical_database/scripts/python/update.py').read())
        exec(open('astronomical_database/scripts/python/update_rdf.py').read(), locals())
