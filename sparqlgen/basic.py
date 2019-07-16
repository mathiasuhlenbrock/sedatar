# coding: utf-8

"""
Basic queries for sparqlgen quepy.
"""

from refo import Group, Question, Plus

from quepy.dsl import HasKeyword
from quepy.parsing import Lemma, Particle, Pos, QuestionTemplate, Token

from dsl import *

class Thing(Particle):
    regex = Plus(Pos("JJ") | Pos("DT") | Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS") | Pos("CD") | Pos('PRP'))

    def interpret(self, match):
        return HasKeyword(match.words.tokens)

class Prop(Particle):
    regex = Pos("NN") | Pos("NNS") | Pos("NNP") | Pos("NNPS")

    def interpret(self, match):
        return match.words.tokens

class WhatIs(QuestionTemplate):
    """
    Regex for questions like "What is ..."
    Ex: "What is a planet?"
    """

    regex = Lemma("what") + Lemma("be") + Question(Pos("DT")) + Thing() + Question(Pos("."))

    def interpret(self, match):
        return IsDefinedIn(match.thing)

class PropertyOfQuestion(QuestionTemplate):
    """
    Regex for questions about various properties of a thing.
    Ex: "What is the size of Jupiter?"
    """

    regex = Pos("WP") + Token("is") + Pos("DT") + Prop() + Pos("IN") + Question(Pos("DT")) + Thing() + Question(Pos("."))

    def interpret(self, match):
        if match.prop == "density":
            return DensityOf(match.thing)

        elif match.prop == "distance":
            return DistanceOf(match.thing)

        elif match.prop == "mass":
            return MassOf(match.thing)

        elif match.prop == "size" or match.prop == "radius":
            return SizeOf(match.thing)