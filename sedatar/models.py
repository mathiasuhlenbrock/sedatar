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
        g = rdflib.Graph()
        g.parse('astronomical_database/data/rdf/astronomical_database.rdf')
        sparqlgen = quepy.install('sparqlgen')
        target, query, metadata = sparqlgen.get_query(self.question_str)
        if not query:
            return 'Query not generated.'
        results = g.query(query)
        if not results:
            return 'No answer found.'
        answer = list()
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
        return '<br>'.join(sorted(answer)) + '.'
