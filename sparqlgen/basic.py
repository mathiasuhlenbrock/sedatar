# coding: utf-8

"""
Basic queries for sparqlgen quepy.
"""

from nltk.stem import WordNetLemmatizer
from quepy.quepy.parsing import Lemma, Particle, Pos, QuestionTemplate, Token
from refo.refo.patterns import Question, Plus
from .dsl import *


class Thing(Particle):
    # TODO: Add also tags for plurals? Add all tag types?
    regex = Plus(
        Pos('JJ') | Pos('DT') | Pos('NN') | Pos('NNP') | Pos('CD') | Pos('PRP') | Pos(':') | Pos('VBG') | Pos('VBN'))

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
        return LabelOf(IsDefinedIn(match.thing)), {'category': 'definition'}


class WhatIsInstance(QuestionTemplate):
    """
    Regex for questions like "What is (the) | are the ...?"
    Ex: "What is Kepler 11 b?"
    """
    regex = Lemma('what') + (
            (Token('is') + Question(Token('the'))) | (Token('are') + Token('the'))) + Thing() + Question(Pos('.'))

    def interpret(self, match):
        return LabelOf(IsInstanceOf(match.thing)), {'category': 'definition'}


class HowMany(QuestionTemplate):
    """
    Regex for questions like "How many ...s are there?"
    Ex: "How many terrestrial planets are there?"
    """
    regex = Lemma('how') + Token('many') + Things() + Token('are') + Token('there') + Question(Pos('.'))

    def interpret(self, match):
        return NumberOf(HasKeyword(match.things)), {'category': 'number'}


class PropertyOf(QuestionTemplate):
    """
    Regex for questions about various properties of a thing.
    Ex: "What is the size of Jupiter?"
    """
    regex = Pos('WP') + Token('is') + Pos('DT') + Prop() + Pos('IN') + Question(Pos('DT')) + Thing() + Question(
        Pos('.'))

    def interpret(self, match):
        if match.prop == 'density':
            return DensityOf(match.thing), {'category': 'density'}
        elif match.prop == 'distance':
            return DistanceOf(match.thing), {'category': 'distance'}
        elif match.prop == 'mass':
            return MassOf(match.thing), {'category': 'mass'}
        elif match.prop == 'radius':
            return RadiusOf(match.thing), {'category': 'radius'}
        elif match.prop == 'size':
            return SizeOf(match.thing), {'category': 'size'}
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
            return LabelOfBiggest(match.thing), {'category': 'label'}
        elif match.superlative == 'closest':
            return LabelOfClosest(match.thing), {'category': 'label'}
        elif match.superlative == 'farthest':
            return LabelOfFarthest(match.thing), {'category': 'label'}
        elif match.superlative == 'smallest':
            return LabelOfSmallest(match.thing), {'category': 'label'}
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
                'instance_type': 'astronomical_object'
            }
        elif match.things == 'class':
            return LabelOf(IsSubTypeOf(Classes())), {
                'category': 'list',
                'instance_type': 'class'
            }
        elif match.things == 'catalogue':
            return LabelOf(IsSubTypeOf(Catalogues())), {
                'category': 'list',
                'instance_type': 'catalogue'
            }
        elif match.things == 'exoplanet':
            return LabelOf(IsSubTypeOf(Exoplanets())), {
                'category': 'list',
                'instance_type': 'exoplanet'
            }
        elif match.things == 'gas giant':
            return LabelOf(IsSubTypeOf(GasGiants())), {
                'category': 'list',
                'instance_type': 'gas_giant'
            }
        elif match.things == 'planetary system':
            return LabelOf(IsSubTypeOf(PlanetarySystems())), {
                'category': 'list',
                'instance_type': 'planetary_system'
            }
        elif match.things == 'planet':
            return LabelOf(IsSubTypeOf(Planets())), {
                'category': 'list',
                'instance_type': 'planet'
            }
        elif match.things == 'property':
            return LabelOf(IsSubTypeOf(Properties())), {
                'category': 'list',
                'instance_type': 'property'
            }
        elif match.things == 'terrestrial planet':
            return LabelOf(IsSubTypeOf(TerrestrialPlanets())), {
                'category': 'list',
                'instance_type': 'terrestrial_planet'
            }
        elif match.things == 'thing':
            return LabelOf(IsSubTypeOf(AllThings())), {
                'category': 'list',
                'instance_type': 'thing'
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
            'instance_type': 'property'
        }
