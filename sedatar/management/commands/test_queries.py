from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        exec(open('sedatar/scripts/python/tests.py').read(), locals())
