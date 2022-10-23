from urllib.error import HTTPError

import rdflib
from SPARQLWrapper import SPARQLWrapper, JSON
from django.db import models

from quepy import quepy


class Database(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    @property
    def page_name(self):
        return self.name.replace(' ', '_')


class Post(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date = models.DateField()
    headline = models.CharField(max_length=200)
    content_left = models.TextField(default='')
    content_right = models.TextField(default='', blank=True)

    def __unicode__(self):
        return self.name


class Search(models.Model):
    question = models.CharField(max_length=200)
    g = rdflib.Graph()
    g.parse('astronomical_database/data/rdf/astronomical_database.rdf')

    # Persistence with SQLAlchemy.
    # store = rdflib.plugin.get("SQLAlchemy", rdflib.store.Store)(identifier=rdflib.URIRef('triplestore'))
    # g = rdflib.Graph(store, identifier=rdflib.URIRef('triplestore'))
    # g.open(rdflib.Literal('postgresql+psycopg2://uhlenbrock:@localhost:5432/postgres'))

    @staticmethod
    def format(answers):
        answers = sorted(answers)
        return answers

    @staticmethod
    def render_answer_definition(result):
        determiner = 'A'
        if result[0][0] in ['a', 'e', 'i', 'o', 'u']:
            determiner = 'An'
        return determiner + ' %s' % result

    @staticmethod
    def render_answer_label(result):
        return '%s' % result

    @staticmethod
    def render_answer_list_item(result, metadata):
        instance_type = metadata.get('instance_type')
        if instance_type == 'catalogue':
            catalogue = '%s' % result
            # return '<a href="/Astronomical_database/List_of_star_catalogues/' \
            #        + catalogue.replace(' ', '_') + '/">' + catalogue + '</a>'
            return catalogue
        elif instance_type == 'class':
            item = '%s' % result
            return item.capitalize()
        elif instance_type == 'exoplanet' \
                or instance_type == 'gas_giant' \
                or instance_type == 'terrestrial_planet' \
                or instance_type == 'planet':
            planet = '%s' % result
            # return '<a href="/Astronomical_database/List_of_planets/' \
            #        + planet.replace(' ', '_') + '/">' + planet + '</a>'
            return planet
        elif instance_type == 'planetary_system':
            planetary_system = '%s' % result
            # return '<a href="/Astronomical_database/List_of_planetary_systems/' \
            #        + planetary_system.replace(' ', '_') + '/">' + planetary_system + '</a>'
            return planetary_system
        elif instance_type == 'property':
            item = '%s' % result
            return item.capitalize()
        else:
            item = '%s' % result
            return item

    @staticmethod
    def render_answer_property(result):
        return '%s' % result

    @property
    def question_str(self):
        return '%s' % self.question

    @property
    def answers(self):
        sparqlgen = quepy.install('sparqlgen')
        target, query, metadata = sparqlgen.get_query(self.question_str)
        answers = list()
        if not query:
            answers.append('Query not generated')
            return self.format(answers)
        results = self.g.query(query)
        if not results:
            answers.append('No answers found')
            return self.format(answers)
        for result in results:
            category = metadata.get('category')
            if category == 'definition':
                answers.append(self.render_answer_definition(result))
            elif category == 'density' \
                    or category == 'distance' \
                    or category == 'mass' \
                    or category == 'number' \
                    or category == 'radius' \
                    or category == 'size':
                answers.append(self.render_answer_property(result))
            elif category == 'label':
                answers.append(self.render_answer_label(result))
            elif category == 'list':
                answers.append(self.render_answer_list_item(result, metadata))
            else:
                answers.append('No method found to render the answers')
        return self.format(answers)


class SearchWikidata(models.Model):
    question = models.CharField(max_length=200)
    g = SPARQLWrapper('https://query.wikidata.org/sparql')

    @staticmethod
    def format(answers):
        if len(answers) == 1 and isinstance(answers[0], str):
            return answers
        answers.sort(key=lambda x: x['relevance'])
        answers = [answer['text'] for answer in answers]
        return answers

    @staticmethod
    def render_answer_definition(result):
        if result and result.get('x0Description'):
            answer = result.get('x0Description').get('value')
            answer = answer[0].upper() + answer[1:] if len(answer) > 1 else answer[0].upper()
            if answer[-1] == '.':
                answer = answer[:-1]
            relevance = int(result.get('x0').get('value').replace('http://www.wikidata.org/entity/Q', ''))
            rendered_answer = {
                'text': '<a href="' + result.get('x0').get('value') + '">' + answer + '</a>',
                'relevance': relevance
            }
            if answer.startswith('Encyclopedia article'):
                return None
            if answer.startswith('Wikimedia disambiguation page'):
                return None
        else:
            return None
        return rendered_answer

    @property
    def question_str(self):
        return '%s' % self.question

    @property
    def answers(self):
        wikidata = quepy.install('wikidata')
        target, query, metadata = wikidata.get_query(self.question_str)
        answers = list()
        if not query:
            answers.append('Query not generated')
            return self.format(answers)
        query = query.replace('".', '"@en.')
        self.g.setQuery(query)
        self.g.setReturnFormat(JSON)
        try:
            results = self.g.query().convert()
        except HTTPError as http_error:
            answers.append('Wikidata says: HTTP Error {}: {}.'.format(http_error.code, http_error.reason))
            return self.format(answers)
        if not results['results']['bindings']:
            answers.append('No answers found')
            return self.format(answers)
        for result in results['results']['bindings']:
            category = metadata.get('category')
            if category == 'definition':
                answer = self.render_answer_definition(result)
                if answer:
                    answers.append(answer)
            else:
                answers.append('No method found to render the answers')
        if not answers:
            answers.append('No answers found')
            return self.format(answers)
        return self.format(answers)
