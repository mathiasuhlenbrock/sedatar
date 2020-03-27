# coding: utf-8

"""
Domain specific language for sparqlgen quepy.
"""

from quepy.quepy.dsl import Expression, FixedRelation, FixedType, HasKeyword
from quepy.quepy.encodingpolicy import encoding_flexible_conversion

HasKeyword.relation = 'rdfs:label'


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


class DensityOf(FixedRelation):
    relation = 'ontology:density'
    reverse = True


class DistanceOf(FixedRelation):
    relation = 'ontology:distance'
    reverse = True


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


class MassOf(FixedRelation):
    relation = 'ontology:mass'
    reverse = True


class NumberOf(FixedRelation):
    relation = 'ontology:numberOfInstances'
    reverse = True


class SizeOf(FixedRelation):
    relation = 'ontology:size'
    reverse = True


class UnknownOf(FixedRelation):
    relation = 'ontology:unknown'
    reverse = True


class AstronomicalObjects(FixedSubType):
    fixedsubtype = '<urn://sedatar.org/astronomical_database/astronomy/Astronomical_Object>'


class Classes(FixedSubType):
    fixedsubtype = '<http://www.w3.org/2000/01/rdf-schema#Class>'


class Unknowns(FixedSubType):
    fixedsubtype = '<>'


class Exoplanets(FixedSubType):
    fixedsubtype = '<urn://sedatar.org/astronomical_database/astronomy/Exoplanet>'


class GasGiants(FixedSubType):
    fixedsubtype = '<urn://sedatar.org/astronomical_database/astronomy/Gas_Giant>'


class PlanetarySystems(FixedSubType):
    fixedsubtype = '<urn://sedatar.org/astronomical_database/astronomy/Planetary_System>'


class Planets(FixedSubType):
    fixedsubtype = '<urn://sedatar.org/astronomical_database/astronomy/Planet>'


class TerrestrialPlanets(FixedSubType):
    fixedsubtype = '<urn://sedatar.org/astronomical_database/astronomy/Terrestrial_Planet>'


class AllThings(FixedSubType):
    fixedsubtype = '<urn://sedatar.org/astronomical_database/common/Thing>'
