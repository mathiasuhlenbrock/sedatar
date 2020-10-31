import rdflib
from django.db import models
from quepy import quepy
# from SPARQLWrapper import SPARQLWrapper, JSON
# from urllib.error import HTTPError


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
    def format(answer):
        answer = sorted(answer)
        answer[-1] += '.'
        return answer

    @staticmethod
    def render_answer_definition(result):
        determiner = 'A'
        if result[0][0] in ['a', 'e', 'i', 'o', 'u']:
            determiner = 'An'
        return determiner + ' %s' % result

    @staticmethod
    def render_answer_list_item(result, metadata):
        instances = metadata.get('instances')
        if instances == 'classes':
            item = '%s' % result
            return item.capitalize()
        elif instances == 'exoplanets' \
                or instances == 'gas_giants' \
                or instances == 'terrestrial_planets' \
                or instances == 'planets':
            planet = '%s' % result
            planet = planet.replace(' ', '_')
            return '<a href="/Astronomical_database/List_of_planets/' \
                   + planet + '/">' + planet + '</>'
        elif instances == 'planetary_systems':
            planetary_system = '%s' % result
            planetary_system = planetary_system.replace(' ', '_')
            return '<a href="/Astronomical_database/List_of_planetary_systems/' \
                   + planetary_system + '/">' + planetary_system + '</>'
        elif instances == 'properties':
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
    def answer(self):
        sparqlgen = quepy.install('sparqlgen')
        target, query, metadata = sparqlgen.get_query(self.question_str)
        answer = list()
        if not query:
            answer.append('Query not generated')
            return self.format(answer)
        results = self.g.query(query)
        if not results:
            answer.append('No answer found')
            return self.format(answer)
        for result in results:
            if metadata == 'definition':
                answer.append(self.render_answer_definition(result))
            elif metadata == 'density' \
                    or metadata == 'distance' \
                    or metadata == 'mass' \
                    or metadata == 'number' \
                    or metadata == 'size':
                answer.append(self.render_answer_property(result))
            elif metadata.get('category') == 'list':
                answer.append(self.render_answer_list_item(result, metadata))
            else:
                answer.append('No method found to render the answer')
        return self.format(answer)

# class Search(models.Model):
#     question = models.CharField(max_length=200)
#     g = SPARQLWrapper('https://query.wikidata.org/sparql')
#
#     @staticmethod
#     def format(answer):
#         answer = sorted(answer)
#         if answer[-1][-1] != '.':
#             answer[-1] += '.'
#         return answer
#
#     @staticmethod
#     def render_answer_definition(result):
#         if result:
#             result = result.get('x0Description').get('value')
#             result = result[0].upper() + result[1:] if len(result) > 1 else result[0].upper()
#             if result.startswith('Wikimedia disambiguation page'):
#                 return None
#             if result[-1] != '.':
#                 result += '.'
#         else:
#             return None
#         return '%s' % result
#
#     @property
#     def question_str(self):
#         return '%s' % self.question
#
#     @property
#     def answer(self):
#         wikidata = quepy.install('wikidata')
#         target, query, metadata = wikidata.get_query(self.question_str)
#         answer = list()
#         if not query:
#             answer.append('Query not generated')
#             return self.format(answer)
#         query = query.replace('".', '"@en.')
#         print(query)
#         self.g.setQuery(query)
#         self.g.setReturnFormat(JSON)
#         try:
#             results = self.g.query().convert()
#         except HTTPError:
#             answer.append('Too many requests')
#             return self.format(answer)
#         if not results["results"]["bindings"]:
#             answer.append('No answer found')
#             return self.format(answer)
#         for result in results["results"]["bindings"]:
#             if metadata == 'definition':
#                 partial_answer = self.render_answer_definition(result)
#                 if partial_answer:
#                     answer.append(partial_answer)
#             else:
#                 answer.append('No method found to render the answer')
#         if not answer:
#             answer.append('No answer found')
#             return self.format(answer)
#         return self.format(answer)
