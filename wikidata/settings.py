# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Settings.
"""

# Generated query language
LANGUAGE = 'sparql'

# NLTK config
NLTK_DATA_PATH = ['nltk_data']  # List of paths with NLTK data

# Encoding config
DEFAULT_ENCODING = 'utf-8'

# Sparql config
SPARQL_PREAMBLE = u""""""

SPARQL_SERVICE = u"""wikibase:label { bd:serviceParam wikibase:language 'en'. }"""
