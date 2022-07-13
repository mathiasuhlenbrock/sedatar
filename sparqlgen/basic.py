# coding: utf-8

"""
Basic queries for sparqlgen quepy.
"""

from nltk.stem import WordNetLemmatizer
from quepy.quepy.parsing import Lemma, Particle, Pos, QuestionTemplate, Token
from refo.refo.patterns import Question, Plus
from .dsl import *


class Thing(Particle):
    regex = Plus(Pos('JJ') | Pos('DT') | Pos('NN') | Pos('NNP') | Pos('CD') | Pos('PRP') | Pos(':'))

    def interpret(self, match):
        return HasKeyword(match.words.tokens)


class Things(Particle):
    regex = Plus(Pos('JJ') | Pos('DT') | Pos('NN') | Pos('NNS') | Pos('NNPS') | Pos('CD') | Pos('PRP'))
    custom_lemmas = {'exoplanets': 'exoplanet'}

    def interpret(self, match):
        token_list = match.words.tokens.split()
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(token_list[-1])
        if token_list[-1] == lemma:
            lemma = self.custom_lemmas[lemma] if self.custom_lemmas[lemma] else lemma
        token_list[-1] = lemma
        tokens = ' '.join(token_list)
        return tokens


class Prop(Particle):
    regex = Pos('NN') | Pos('NNS') | Pos('NNP') | Pos('NNPS')

    def interpret(self, match):
        return match.words.tokens


class Superlative(Particle):
    regex = Pos('JJS') | Pos('RBS')

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
        elif match.prop == 'radius':
            return RadiusOf(match.thing), 'radius'
        elif match.prop == 'size':
            return SizeOf(match.thing), 'size'
        else:
            return UnknownOf(match.thing)


class ExtremePropertyOf(QuestionTemplate):
    """
    Regex for questions about extremal property values of a thing.
    Ex: "What is the smallest planet?"
    """
    regex = Pos('WP') + Token('is') + Pos('DT') + Superlative() + Thing() + Question(Pos('.'))

    def interpret(self, match):
        if match.superlative == 'biggest' or match.superlative == 'largest':
            return LabelOfBiggest(match.thing), 'label'
        elif match.superlative == 'closest':
            return LabelOfClosest(match.thing), 'label'
        elif match.superlative == 'farthest':
            return LabelOfFarthest(match.thing), 'label'
        elif match.superlative == 'smallest':
            return LabelOfSmallest(match.thing), 'label'
        else:
            return UnknownOf(match.thing)


class List(QuestionTemplate):
    """
    Regex for commands like "List all ...s!"
    Ex: "List all terrestrial planets!"
    """
    regex = Token('List') + Token('all') + Things() + Question(Pos('.'))

    def interpret(self, match):
        if match.things == 'astronomical object':
            return LabelOf(IsSubTypeOf(AstronomicalObjects())), {
                'category': 'list',
                'instances': 'astronomical_objects'
            }
        elif match.things == 'class':
            return LabelOf(IsSubTypeOf(Classes())), {
                'category': 'list',
                'instances': 'classes'
            }
        elif match.things == 'exoplanet':
            return LabelOf(IsSubTypeOf(Exoplanets())), {
                'category': 'list',
                'instances': 'exoplanets'
            }
        elif match.things == 'gas giant':
            return LabelOf(IsSubTypeOf(GasGiants())), {
                'category': 'list',
                'instances': 'gas_giants'
            }
        elif match.things == 'planetary system':
            return LabelOf(IsSubTypeOf(PlanetarySystems())), {
                'category': 'list',
                'instances': 'planetary_systems'
            }
        elif match.things == 'planet':
            return LabelOf(IsSubTypeOf(Planets())), {
                'category': 'list',
                'instances': 'planets'
            }
        elif match.things == 'property':
            return LabelOf(IsSubTypeOf(Properties())), {
                'category': 'list',
                'instances': 'properties'
            }
        elif match.things == 'terrestrial planet':
            return LabelOf(IsSubTypeOf(TerrestrialPlanets())), {
                'category': 'list',
                'instances': 'terrestrial_planets'
            }
        elif match.things == 'thing':
            return LabelOf(IsSubTypeOf(AllThings())), {
                'category': 'list',
                'instances': 'things'
            }
        else:
            return LabelOf(IsSubTypeOf(Unknowns()))


class ListProperties(QuestionTemplate):
    """
    Regex for commands like "List all properties of a/an ...!"
    Ex: "List all properties of a planet!"
    """
    regex = Token('List') + Token('all') + Token('properties') + Token('of') + Question(Pos('DT')) + Thing() + \
        Question(Pos('.'))

    def interpret(self, match):
        return AllProperties(match.thing), {
            'category': 'list',
            'instances': 'properties'
        }
