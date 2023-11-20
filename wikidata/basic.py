# coding: utf-8

"""
Basic queries for wikidata quepy.
"""

from nltk.stem import WordNetLemmatizer
from quepy.quepy.parsing import Lemma, Particle, Pos, QuestionTemplate, Token
from refo.refo.patterns import Question, Plus
from .dsl import *


class Thing(Particle):
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


class WhatIsClass(QuestionTemplate):
    """
    Regex for questions like "What is a/an | are ...?"
    Ex: "What is a planet?"
    """
    regex = Lemma('what') + (
            (Token('is') + Question((Token('a') | Token('an'))) + Thing()) | (Token('are') + Things())) + Question(
        Pos('.'))

    def interpret(self, match):
        if hasattr(match, 'thing'):
            return HasKeyword(match.thing), {'category': 'definition'}
        elif hasattr(match, 'things'):
            return HasKeyword(match.things), {'category': 'definition'}


class WhatIsInstance(QuestionTemplate):
    """
    Regex for questions like "What is | are (the) ...?"
    Ex: "What is Kepler 11 b?"
    """
    regex = Lemma('what') + (Token('is') | Token('are')) + Question(Token('the')) + Thing() + Question(Pos('.'))

    def interpret(self, match):
        return HasKeyword(match.thing), {'category': 'definition'}


class List(QuestionTemplate):
    """
    Regex for commands like "List all ...s!"
    Ex: "List all terrestrial planets!"
    """
    regex = Token('List') + Token('all') + Things() + Question(Pos('.'))

    def interpret(self, match):
        fixedsubtype_components = [component for component in match.things.split()]
        fixedsubtype = ' '.join(fixedsubtype_components)
        return IsInstanceOf(HasKeyword(fixedsubtype)), {
            'category': 'list',
            'instance_type': match.things.replace(' ', '_')
        }
