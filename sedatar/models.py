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
        return determiner + ' %s.' % result

    @staticmethod
    def render_answer_density(result):
        unit = 'g/cm&sup3;'
        return '%s ' % result + unit + '.'

    @staticmethod
    def render_answer_distance(result):
        unit = 'ly'
        return '%s ' % result + unit + '.'

    @staticmethod
    def render_answer_mass(result):
        unit = 'M<sub>&#9795;</sub>'
        return '%s ' % result + unit + '.'

    @staticmethod
    def render_answer_size(result):
        unit = 'R<sub>&#9795;</sub>'
        return '%s ' % result + unit + '.'

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
        for result in results:
            if metadata == 'definition':
                return self.render_answer_definition(result)
            elif metadata == 'density':
                return self.render_answer_density(result)
            elif metadata == 'distance':
                return self.render_answer_distance(result)
            elif metadata == 'mass':
                return self.render_answer_mass(result)
            elif metadata == 'size':
                return self.render_answer_size(result)
            else:
                return 'No method found to render the answer.'
