# coding: utf-8

"""
Domain specific language for sparqlgen quepy.
"""

from quepy.quepy.dsl import FixedRelation, HasKeyword

HasKeyword.relation = "rdfs:label"


class DensityOf(FixedRelation):
    relation = "ontology:density"
    reverse = True


class DistanceOf(FixedRelation):
    relation = "ontology:distance"
    reverse = True


class IsDefinedIn(FixedRelation):
    relation = "rdfs:subClassOf"
    reverse = True


class IsInstanceOf(FixedRelation):
    relation = "rdf:type"
    reverse = True


class LabelOf(FixedRelation):
    relation = "rdfs:label"
    reverse = True


class MassOf(FixedRelation):
    relation = "ontology:mass"
    reverse = True


class SizeOf(FixedRelation):
    relation = "ontology:size"
    reverse = True
