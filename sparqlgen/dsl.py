# coding: utf-8

"""
Domain specific language for sparqlgen quepy.
"""

from quepy.quepy.dsl import FixedRelation, FixedType, HasKeyword

HasKeyword.relation = 'rdfs:label'


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


class Classes(FixedType):
    fixedtype = '<http://www.w3.org/2000/01/rdf-schema#Class>'


class Unknowns(FixedType):
    fixedtype = '<>'


class Exoplanets(FixedType):
    fixedtype = '<urn://sedatar.org/astronomical_database/astronomy/Exoplanet>'


class GasGiants(FixedType):
    fixedtype = '<urn://sedatar.org/astronomical_database/astronomy/Gas_Giant>'


class PlanetarySystems(FixedType):
    fixedtype = '<urn://sedatar.org/astronomical_database/astronomy/Planetary_System>'


class TerrestrialPlanets(FixedType):
    fixedtype = '<urn://sedatar.org/astronomical_database/astronomy/Terrestrial_Planet>'
