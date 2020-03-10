"""
Documentation goes here.
"""

# import rdflib
from lxml import etree
from subprocess import call
from astronomical_database.models import Planet, PlanetarySystem

number_of_terrestrial_planets = 0
number_of_gas_giants = 0
for planet in Planet.objects.all():
    outputFile = open(
        "astronomical_database/data/rdf/individuals/"
        + planet.name.replace(' ', '_')
        + ".rdf",
        'w'
    )
    outputFile.write(
        "<rdf:Description rdf:about=\"urn://sedatar.org/astronomical_database/individuals/"
        + planet.name.replace(' ', '_') + "\">\n"
    )
    if planet.classification == 'Terrestrial planet':
        number_of_terrestrial_planets += 1
        outputFile.write(
            "  <rdf:type rdf:resource=\"urn://sedatar.org/astronomical_database/astronomy/Terrestrial_Planet\" />\n"
        )
    elif planet.classification == 'Gas giant':
        number_of_gas_giants += 1
        outputFile.write(
            "  <rdf:type rdf:resource=\"urn://sedatar.org/astronomical_database/astronomy/Gas_Giant\" />\n"
        )
    else:
        outputFile.write(
            "  <rdf:type rdf:resource=\"urn://sedatar.org/astronomical_database/astronomy/Exoplanet\" />\n"
        )
    outputFile.write(
        "  <rdfs:label>" + planet.name.replace('-', ' ') + "</rdfs:label>\n"
    )
    if planet.system.host_distance_ly:
        outputFile.write("  <ontology:distance rdf:datatype=\"http://www.w3.org/2001/XMLSchema#float\">"
                         + str(planet.system.host_distance_ly) + " " + "ly" + "</ontology:distance>\n")
    if planet.radius:
        outputFile.write("  <ontology:size rdf:datatype=\"http://www.w3.org/2001/XMLSchema#float\">"
                         + str(planet.radius) + " " + "R&lt;sub&gt;&#9795;&lt;/sub&gt;" + "</ontology:size>\n")
    if planet.mass:
        outputFile.write("  <ontology:mass rdf:datatype=\"http://www.w3.org/2001/XMLSchema#float\">"
                         + str(planet.mass) + " " + "M&lt;sub&gt;&#9795;&lt;/sub&gt;" + "</ontology:mass>\n")
    if planet.density:
        outputFile.write("  <ontology:density rdf:datatype=\"http://www.w3.org/2001/XMLSchema#float\">"
                         + str(planet.density) + " " + "g/cm&#179;" + "</ontology:density>\n")
    if planet.semimajoraxis:
        outputFile.write("  <ontology:semimajoraxis rdf:datatype=\"http://www.w3.org/2001/XMLSchema#float\">"
                         + str(planet.semimajoraxis) + " " + "AU" + "</ontology:semimajoraxis>\n")
    outputFile.write("</rdf:Description>")
    outputFile.close()

for planetarySystem in PlanetarySystem.objects.all():
    outputFile = open(
        "astronomical_database/data/rdf/individuals/"
        + planetarySystem.name.replace(' ', '_')
        + ".rdf",
        'w'
    )
    outputFile.write(
        "<rdf:Description rdf:about=\"urn://sedatar.org/astronomical_database/individuals/"
        + planetarySystem.name.replace(' ', '_')
        + "\">\n"
    )
    outputFile.write(
        "  <rdf:type rdf:resource=\"urn://sedatar.org/astronomical_database/astronomy/Planetary_System\" />\n"
    )
    outputFile.write(
        "  <rdfs:label>" + planetarySystem.name.replace('-', ' ') + "</rdfs:label>\n"
    )
    if planetarySystem.host_distance_ly:
        outputFile.write("  <ontology:distance rdf:datatype=\"http://www.w3.org/2001/XMLSchema#float\">"
                         + str(planetarySystem.host_distance_ly) + " " + "ly" + "</ontology:distance>\n")
    if planetarySystem.number_of_planets:
        outputFile.write("  <ontology:numberofplanets rdf:datatype=\"http://www.w3.org/2001/XMLSchema#integer\">"
                         + str(planetarySystem.number_of_planets) + "</ontology:numberofplanets>\n")
    if planetarySystem.max_planet_semimajoraxis and planetarySystem.max_planet_semimajoraxis != 1.:
        outputFile.write("  <ontology:size rdf:datatype=\"http://www.w3.org/2001/XMLSchema#float\">"
                         + str(planetarySystem.max_planet_semimajoraxis) + " " + "AU" + "</ontology:size>\n")
    outputFile.write("</rdf:Description>")
    outputFile.close()


def insert_number_of_instances(namespace, entity, number_of_instances):
    file_name = 'astronomical_database/data/rdf/astronomical_database.rdf'
    rdf_file = open(file_name)
    rdf_data = rdf_file.read()
    root_element = etree.fromstring(rdf_data)
    target_element = root_element.xpath(
        '//rdf:Description[@rdf:about="urn://sedatar.org/astronomical_database/' + namespace + '/'
        + entity + '"]/ontology:numberOfInstances',
        namespaces={
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'ontology': 'urn://sedatar.org/'
        }
    )
    target_element[0].text = str(number_of_instances)
    etree.ElementTree(root_element).write(file_name, pretty_print=True)


call(["astronomical_database/scripts/shell/update_astronomical_database_rdf.sh"])

number_of_planets = Planet.objects.all().count()
number_of_planetary_systems = PlanetarySystem.objects.all().count()
insert_number_of_instances('astronomy', 'Planet', number_of_planets)
insert_number_of_instances('astronomy', 'Terrestrial_Planet', number_of_terrestrial_planets)
insert_number_of_instances('astronomy', 'Gas_Giant', number_of_gas_giants)
insert_number_of_instances('astronomy', 'Planetary_System', number_of_planetary_systems)
insert_number_of_instances('astronomy', 'Astronomical_Object', number_of_planets + number_of_planetary_systems)
insert_number_of_instances('astronomy', 'Exoplanet', number_of_planets - 8)
insert_number_of_instances('common', 'Thing', number_of_planets + number_of_planetary_systems)

# Persistence with Sleepycat.
# G = rdflib.ConjunctiveGraph('Sleepycat')
# G.open('astronomical_database/data/rdf/triplestore', create=True)
# G.parse("astronomical_database/data/rdf/astronomical_database.rdf")
# G.close()

# Persistence with SQLAlchemy. Don't forget to install rdflib-sqlalchemy.
# store = rdflib.plugin.get("SQLAlchemy", rdflib.store.Store)(identifier=rdflib.URIRef('triplestore'))
# G = rdflib.Graph(store, identifier=rdflib.URIRef('triplestore'))
# # G.open(rdflib.Literal('sqlite://'), create=True) # In Memory!
# G.open(rdflib.Literal('postgresql+psycopg2://uhlenbrock:@localhost:5432/postgres'), create=True)
# G.parse("astronomical_database/data/rdf/astronomical_database.rdf")
# G.close()
