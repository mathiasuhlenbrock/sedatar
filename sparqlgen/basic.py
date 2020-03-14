# coding: utf-8

"""
Basic queries for sparqlgen quepy.
"""

from nltk.stem import WordNetLemmatizer
from refo import Question, Plus
from quepy.quepy.parsing import Lemma, Particle, Pos, QuestionTemplate, Token
from .dsl import *


class Thing(Particle):
    regex = Plus(Pos('JJ') | Pos('DT') | Pos('NN') | Pos('NNP') | Pos('CD') | Pos('PRP'))

    def interpret(self, match):
        return HasKeyword(match.words.tokens)


class Things(Particle):
    regex = Plus(Pos('JJ') | Pos('DT') | Pos('NN') | Pos('NNS') | Pos('NNPS') | Pos('CD') | Pos('PRP'))

    def interpret(self, match):
        token_list = match.words.tokens.split()
        wnl = WordNetLemmatizer()
        token_list[-1] = wnl.lemmatize(token_list[-1])
        tokens = ' '.join(token_list)
        return tokens


class Prop(Particle):
    regex = Pos('NN') | Pos('NNS') | Pos('NNP') | Pos('NNPS')

    def interpret(self, match):
        return match.words.tokens


class WhatIsClass(QuestionTemplate):
    """
    Regex for questions like "What is a/an | are ...?"
    Ex: "What is a planet?"
    """
    regex = Lemma('what') + (Token('is') + (Token('a') | Token('an')) | Token('are')) + Thing() + Question(Pos('.'))

    def interpret(self, match):
        return LabelOf(IsDefinedIn(match.thing)), 'definition'


class WhatIsInstance(QuestionTemplate):
    """
    Regex for questions like "What is (the) | are the ...?"
    Ex: "What is Kepler 11 b?"
    """
    regex = Lemma('what') + (
            (Token('is') + Question(Token('the'))) | (Token('are') + Token('the'))) + Thing() + Question(Pos('.'))

    def interpret(self, match):
        return LabelOf(IsInstanceOf(match.thing)), 'definition'


class HowMany(QuestionTemplate):
    """
    Regex for questions like "How many ...s are there?"
    Ex: "How many terrestrial planets are there?"
    """
    regex = Lemma('how') + Token('many') + Things() + Token('are') + Token('there') + Question(Pos('.'))

    def interpret(self, match):
        return NumberOf(HasKeyword(match.things)), 'number'


class PropertyOf(QuestionTemplate):
    """
    Regex for questions about various properties of a thing.
    Ex: "What is the size of Jupiter?"
    """
    regex = Pos('WP') + Token('is') + Pos('DT') + Prop() + Pos('IN') + Question(Pos('DT')) + Thing() + Question(
        Pos('.'))

    def interpret(self, match):
        if match.prop == 'density':
            return DensityOf(match.thing), 'density'
        elif match.prop == 'distance':
            return DistanceOf(match.thing), 'distance'
        elif match.prop == 'mass':
            return MassOf(match.thing), 'mass'
        elif match.prop == 'size' or match.prop == 'radius':
            return SizeOf(match.thing), 'size'
        else:
            return UnknownOf(match.thing)


class List(QuestionTemplate):
    """
    Regex for commands like "List all ...s!"
    Ex: "List all terrestrial planets!"
    """
    regex = Token('List') + Token('all') + Things() + Question(Pos('.'))

    def interpret(self, match):
        if match.things == 'class':
            return LabelOf(Classes()), 'list'
        elif match.things == 'exoplanet':
            return LabelOf(Exoplanets()), 'list'
        elif match.things == 'gas giant':
            return LabelOf(GasGiants()), 'list'
        elif match.things == 'planetary system':
            return LabelOf(PlanetarySystems()), 'list'
        elif match.things == 'terrestrial planet':
            return LabelOf(TerrestrialPlanets()), 'list'
        else:
            return LabelOf(Unknowns())
