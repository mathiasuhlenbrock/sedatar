# coding: utf-8

"""
Domain specific language for wikidata quepy.
"""

from quepy.quepy.dsl import FixedRelation, HasKeyword

HasKeyword.relation = 'rdfs:label'


class IsDefinedIn(FixedRelation):
    relation = 'wdt:P279'
    reverse = True
