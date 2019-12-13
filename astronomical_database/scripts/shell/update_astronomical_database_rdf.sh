#!/bin/bash

cd astronomical_database/data/rdf/ || exit
cat astronomy/* common/* individuals/* > astronomical_database.intermediate.rdf
awk 'BEGIN {print "<?xml version=\"1.0\"?>\n<rdf:RDF\n  xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n  xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\"\n  xmlns:ontology=\"urn://sedatar.org/\"\n>"} {print} END {print "</rdf:RDF>"}' astronomical_database.intermediate.rdf > astronomical_database.rdf
rm astronomical_database.intermediate.rdf
cd - || exit
