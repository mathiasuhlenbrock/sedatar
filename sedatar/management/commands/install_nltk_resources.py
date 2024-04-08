import nltk
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')