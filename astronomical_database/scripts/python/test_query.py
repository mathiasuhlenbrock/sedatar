import rdflib

g = rdflib.Graph()
g.parse('astronomical_database/data/rdf/astronomical_database.rdf')
result = g.query("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ontology: <urn://sedatar.org/astronomical_database#>

    # All classes.
    SELECT DISTINCT ?x1 WHERE {
        ?x0 rdf:type rdfs:Class.
        ?x0 rdfs:label ?x1.
    }

    # All properties.
    # SELECT DISTINCT ?x2 WHERE {
    #     ?x0 rdfs:subClassOf* rdf:Property.
    #     ?x1 rdf:type ?x0.
    #     ?x1 rdfs:label ?x2.
    # }

    # All terrestrial planets.
    # SELECT DISTINCT ?x1 WHERE {
    #     # ?x0 rdfs:label 'terrestrial planet'.
    #     # ?x0 rdf:type ?x1.
    #     ?x0 rdf:type ontology:Terrestrial_Planet.
    #     ?x0 rdfs:label ?x1.
    # }

    # All things.
    # SELECT DISTINCT ?x2 WHERE {
    #     ?x0 rdfs:subClassOf* ontology:Thing.
    #     ?x1 rdf:type ?x0.
    #     ?x1 rdfs:label ?x2.
    # }

    # Number of planets.
    # SELECT DISTINCT ?x1 WHERE {
    #     ?x0 rdfs:label 'planet'.
    #     ?x0 ontology:numberOfInstances ?x1.
    # }

    # Size of Earth.
    # SELECT DISTINCT ?x2 WHERE {
    #     ?x0 rdfs:label 'Earth'.
    #     ?x0 ?x1 ?x2.
    #     ?x1 rdfs:subPropertyOf* ontology:size.
    # }
""")
for row in sorted(result):
    print('%s' % row)
