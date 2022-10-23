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


class WhatIsClass(QuestionTemplate):
    """
    Regex for questions like "What is a/an | are ...?"
    Ex: "What is a planet?"
    """
    regex = Lemma('what') + (Token('is') + Question((Token('a') | Token('an'))) + Thing() | Token('are') + Things()) + \
            Question(Pos('.'))

    def interpret(self, match):
        if hasattr(match, 'thing'):
            return match.thing, {'category': 'definition'}
        elif hasattr(match, 'things'):
            return match.things, {'category': 'definition'}
