# coding: utf-8

"""
Domain specific language for sparqlgen quepy.
"""

from quepy.quepy.dsl import Expression, FixedRelation, HasKeyword
from quepy.quepy.encodingpolicy import encoding_flexible_conversion

HasKeyword.relation = 'rdfs:label'


class FixedSubProperty(Expression):
    """
    Expression for a fixed subproperty.
    """

    fixedsubpropertyrelation = u'rdfs:subPropertyOf*'

    def __init__(self, prefix, fixedsubproperty, data):
        super(FixedSubProperty, self).__init__()
        self.fixedsubproperty = prefix + ':' + fixedsubproperty
        self.fixedsubproperty = encoding_flexible_conversion(self.fixedsubproperty)
        self.fixedsubpropertyrelation = \
            encoding_flexible_conversion(self.fixedsubpropertyrelation)
        # TODO: Improve the following lines.
        self.merge(data)
        self.nodes.append([])
        self.head += 1
        self.add_data(self.fixedsubpropertyrelation, self.fixedsubproperty)
        self.nodes[0].append(('?x1', 2))
        self.head += 1


class FixedSubType(Expression):
    """
    Expression for a fixed subtype.
    """

    fixedsubtyperelation = u'rdfs:subClassOf*'

    def __init__(self, prefix, fixedsubtype):
        super(FixedSubType, self).__init__()
        self.fixedsubtype = prefix + ':' + fixedsubtype
        self.fixedsubtype = encoding_flexible_conversion(self.fixedsubtype)
        self.fixedsubtyperelation = \
            encoding_flexible_conversion(self.fixedsubtyperelation)
        self.add_data(self.fixedsubtyperelation, self.fixedsubtype)


class IsDefinedIn(FixedRelation):
    relation = 'rdfs:subClassOf'
    reverse = True


class IsInstanceOf(FixedRelation):
    relation = 'rdf:type'
    reverse = True


class IsSubTypeOf(FixedRelation):
    relation = 'rdf:type'


class LabelOf(FixedRelation):
    relation = 'rdfs:label'
    reverse = True


class NumberOf(FixedRelation):
    relation = 'ontology:numberOfInstances'
    reverse = True


class UnknownOf(FixedRelation):
    relation = 'ontology:unknown'
    reverse = True


class AllProperties(Expression):
    """
    """

    def __init__(self, data):
        super(AllProperties, self).__init__()
        self.merge(data)
        self.nodes[0].append(('?x1', 2))
        self.nodes.append([('rdfs:label', 3)])
        self.nodes.append([])
        self.head += 3
