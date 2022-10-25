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
        return match.words.tokens


class Things(Particle):
    regex = Plus(Pos('JJ') | Pos('DT') | Pos('NN') | Pos('NNS') | Pos('NNPS') | Pos('CD') | Pos('PRP'))
    custom_lemmas = {'exoplanets': 'exoplanet'}

    def interpret(self, match):
        token_list = match.words.tokens.split()
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(token_list[-1])
        if token_list[-1] == lemma and lemma in self.custom_lemmas:
            lemma = self.custom_lemmas[lemma]
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
    Regex for questions like "What is a/an ...?"
    Ex: "What is a planet?"
    """
    regex = Lemma('what') + Token('is') + (Token('a') | Token('an')) + Thing() + Question(Pos('.'))

    def interpret(self, match):
        return LabelOf(IsDefinedIn(HasKeyword(match.thing))), {'category': 'definition'}


class WhatIsInstance(QuestionTemplate):
    """
    Regex for questions like "What is (the) ...?"
    Ex: "What is Kepler 11 b?"
    """
    regex = Lemma('what') + Token('is') + Question(Token('the')) + Thing() + Question(Pos('.'))

    def interpret(self, match):
        return LabelOf(IsInstanceOf(HasKeyword(match.thing))), {'category': 'definition'}


class HowMany(QuestionTemplate):
    """
    Regex for questions like "How many ...s are there?"
    Ex: "How many terrestrial planets are there?"
    """
    regex = Lemma('how') + Token('many') + Things() + Token('are') + Token('there') + Question(Pos('.'))

    def interpret(self, match):
        return NumberOf(HasKeyword(match.things)), {'category': 'property'}


class PropertyOf(QuestionTemplate):
    """
    Regex for questions about various properties of a thing.
    Ex: "What is the size of Jupiter?"
    """
    regex = Pos('WP') + Token('is') + Pos('DT') + Prop() + Pos('IN') + Question(Pos('DT')) + Thing() + Question(
        Pos('.'))

    def interpret(self, match):
        fixedsubproperty = match.prop
        return FixedSubProperty('ontology', fixedsubproperty, HasKeyword(match.thing)), {'category': 'property'}


class ExtremePropertyOf(QuestionTemplate):
    """
    Regex for questions about extremal property values of a thing.
    Ex: "What is the smallest planet?"
    """
    regex = Pos('WP') + Token('is') + Pos('DT') + Superlative() + Thing() + Question(Pos('.'))

    def interpret(self, match):
        if match.superlative == 'biggest' or match.superlative == 'largest':
            return FixedSubProperty('ontology', 'maxSizeInstance', HasKeyword(match.thing)), {'category': 'label'}
        elif match.superlative == 'closest':
            return FixedSubProperty('ontology', 'minDistanceInstance', HasKeyword(match.thing)), {'category': 'label'}
        elif match.superlative == 'farthest':
            return FixedSubProperty('ontology', 'maxDistanceInstance', HasKeyword(match.thing)), {'category': 'label'}
        elif match.superlative == 'smallest':
            return FixedSubProperty('ontology', 'minSizeInstance', HasKeyword(match.thing)), {'category': 'label'}
        else:
            return UnknownOf(HasKeyword(match.thing))


class List(QuestionTemplate):
    """
    Regex for commands like "List all ...s!"
    Ex: "List all terrestrial planets!"
    """
    regex = Token('List') + Token('all') + Things() + Question(Pos('.'))

    def interpret(self, match):
        if match.things == 'class':
            fixedsubtype = match.things.capitalize()
            return LabelOf(IsSubTypeOf(FixedSubType('rdfs', fixedsubtype))), {
                'category': 'list',
                'instance_type': 'class'
            }
        elif match.things == 'property':
            fixedsubtype = match.things.capitalize()
            return LabelOf(IsSubTypeOf(FixedSubType('rdf', fixedsubtype))), {
                'category': 'list',
                'instance_type': 'property'
            }
        else:
            fixedsubtype_components = [component.capitalize() for component in match.things.split()]
            fixedsubtype = '_'.join(fixedsubtype_components)
            return LabelOf(IsSubTypeOf(FixedSubType('ontology', fixedsubtype))), {
                'category': 'list',
                'instance_type': match.things.replace(' ', '_')
            }


class ListProperties(QuestionTemplate):
    """
    Regex for commands like "List all properties of a/an ...!"
    Ex: "List all properties of a planet!"
    """
    regex = Token('List') + Token('all') + Token('properties') + Token('of') + Question(Pos('DT')) + Thing() + Question(
        Pos('.'))

    def interpret(self, match):
        return AllProperties(HasKeyword(match.thing)), {
            'category': 'list',
            'instance_type': 'property'
        }
