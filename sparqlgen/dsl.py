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

    fixedsubproperty = None
    fixedsubpropertyrelation = u'rdfs:subPropertyOf*'

    def __init__(self, data):
        super(FixedSubProperty, self).__init__()
        if self.fixedsubproperty is None:
            raise ValueError('You *must* define the `fixedtype` '
                             'class attribute to use this class.')
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

    fixedsubtype = None
    fixedsubtyperelation = u'rdfs:subClassOf*'

    def __init__(self):
        super(FixedSubType, self).__init__()
        if self.fixedsubtype is None:
            raise ValueError('You *must* define the `fixedtype` '
                             'class attribute to use this class.')
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


class DensityOf(FixedSubProperty):
    fixedsubproperty = 'ontology:density'


class DistanceOf(FixedSubProperty):
    fixedsubproperty = 'ontology:distance'


class LabelOfBiggest(FixedSubProperty):
    fixedsubproperty = 'ontology:maxSizeInstance'


class LabelOfClosest(FixedSubProperty):
    fixedsubproperty = 'ontology:minDistanceInstance'


class LabelOfFarthest(FixedSubProperty):
    fixedsubproperty = 'ontology:maxDistanceInstance'


class LabelOfSmallest(FixedSubProperty):
    fixedsubproperty = 'ontology:minSizeInstance'


class MassOf(FixedSubProperty):
    fixedsubproperty = 'ontology:mass'


class RadiusOf(FixedSubProperty):
    fixedsubproperty = 'ontology:radius'


class SizeOf(FixedSubProperty):
    fixedsubproperty = 'ontology:size'


class AstronomicalObjects(FixedSubType):
    fixedsubtype = 'ontology:Astronomical_Object'


class Catalogues(FixedSubType):
    fixedsubtype = 'ontology:Catalogue'


class Classes(FixedSubType):
    fixedsubtype = 'rdfs:Class'


class Unknowns(FixedSubType):
    fixedsubtype = 'ontology:unknown'


class Exoplanets(FixedSubType):
    fixedsubtype = 'ontology:Exoplanet'


class GasGiants(FixedSubType):
    fixedsubtype = 'ontology:Gas_Giant'


class PlanetarySystems(FixedSubType):
    fixedsubtype = 'ontology:Planetary_System'


class Planets(FixedSubType):
    fixedsubtype = 'ontology:Planet'


class Properties(FixedSubType):
    fixedsubtype = 'rdf:Property'


class TerrestrialPlanets(FixedSubType):
    fixedsubtype = 'ontology:Terrestrial_Planet'


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


class AllThings(FixedSubType):
    fixedsubtype = 'ontology:Thing'
