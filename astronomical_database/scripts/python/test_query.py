import rdflib

g = rdflib.Graph()
g.parse('astronomical_database/data/rdf/astronomical_database.rdf')
result = g.query("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ontology: <urn://sedatar.org/>

    # All classes.
    SELECT DISTINCT ?x1 WHERE {
        ?x0 rdf:type <http://www.w3.org/2000/01/rdf-schema#Class>.
        ?x0 rdfs:label ?x1.
    }

    # All terrestrial planets.
    # SELECT DISTINCT ?x1 WHERE {
    #     # ?x0 rdfs:label 'terrestrial planet'.
    #     # ?x0 rdf:type ?x1.
    #     ?x0 rdf:type <urn://sedatar.org/astronomical_database/astronomy/Terrestrial_Planet>.
    #     ?x0 rdfs:label ?x1.
    # }

    # Number of planets.
    # SELECT DISTINCT ?x1 WHERE {
    #     ?x0 rdfs:label "planet".
    #     ?x0 ontology:numberOfInstances ?x1.
    # }
""")
for row in sorted(result):
    print('%s' % row)
