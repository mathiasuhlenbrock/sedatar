import rdflib
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
    def render_answer_list_item(result):
        return '%s' % result

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
            elif metadata == 'list':
                answer.append(self.render_answer_list_item(result).capitalize())
            else:
                answer.append('No method found to render the answer')
        return self.format(answer)
