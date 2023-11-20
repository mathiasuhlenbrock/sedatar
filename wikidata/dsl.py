# coding: utf-8

"""
Domain specific language for wikidata quepy.
"""

from quepy.quepy.dsl import Expression, FixedRelation, HasKeyword
from quepy.quepy.encodingpolicy import encoding_flexible_conversion

HasKeyword.relation = 'rdfs:label'


class FixedSubType(Expression):
    """
    Expression for a fixed subtype.
    """

    fixedsubtyperelation = u'wdt:P31'

    def __init__(self, fixedsubtype):
        super(FixedSubType, self).__init__()
        self.fixedsubtype = fixedsubtype
        self.fixedsubtype = encoding_flexible_conversion(self.fixedsubtype)
        self.fixedsubtyperelation = \
            encoding_flexible_conversion(self.fixedsubtyperelation)
        self.add_data(self.fixedsubtyperelation, self.fixedsubtype)


class IsDefinedIn(FixedRelation):
    relation = 'wdt:P279'
    reverse = True


class IsInstanceOf(FixedRelation):
    relation = 'wdt:P31'


class IsSubTypeOf(FixedRelation):
    relation = 'rdf:type'


class LabelOf(FixedRelation):
    relation = 'rdfs:label'
    reverse = True
