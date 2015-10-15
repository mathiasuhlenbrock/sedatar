from django.db import models

import quepy
import sparqlgen
import rdflib

class Database(models.Model):
    name  = models.CharField(max_length = 200)
    image = models.CharField(max_length = 200)

    def __unicode__(self):
       return self.name

    @property
    def page_name(self):
        return self.name.replace(" ", "_")

class Post(models.Model):
    name          = models.CharField(max_length = 200)
    author        = models.CharField(max_length = 200)
    date          = models.DateField()
    headline      = models.CharField(max_length = 200)
    content_left  = models.TextField(default = "")
    content_right = models.TextField(default = "", blank = True)

    def __unicode__(self):
       return self.name

class Search(models.Model):
    question = models.CharField(max_length = 200)

    @property
    def question_str(self):
        return '%s' % self.question

    @property
    def answer(self):
        g = rdflib.Graph()
        g.parse("astronomical_database/data/rdf/astronomical_database.rdf")

        sparqlgen = quepy.install("sparqlgen")

        target, query, metadata = sparqlgen.get_query(self.question_str)

        if query:
            results = g.query(query)
            if results:
                for result in results:
                    return '%s' % result
            else:
                return "No answer found."
        else:
            return "Query not generated."
