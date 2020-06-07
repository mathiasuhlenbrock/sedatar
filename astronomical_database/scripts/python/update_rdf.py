"""
Documentation goes here.
"""

# import rdflib
from lxml import etree
from astronomical_database.models import Planet, PlanetarySystem


def insert_number_of_instances(root, namespace, entity, number_of_instances):
    target_element = root.xpath(
        '//rdf:Description[@rdf:about="urn://sedatar.org/astronomical_database/' + namespace + '/'
        + entity + '"]/ontology:numberOfInstances',
        namespaces={
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'ontology': 'urn://sedatar.org/'
        }
    )
    target_element[0].text = str(number_of_instances)


file_name = 'astronomical_database/data/rdf/astronomical_database.rdf'
rdf_file = open(file_name, 'w')

FLOAT_NAMESPACE = 'http://www.w3.org/2001/XMLSchema#float'
RDF_NAMESPACE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
RDFS_NAMESPACE = 'http://www.w3.org/2000/01/rdf-schema#'
ONTOLOGY_NAMESPACE = 'urn://sedatar.org/'
RDF = '{%s}' % RDF_NAMESPACE
RDFS = '{%s}' % RDFS_NAMESPACE
ONTOLOGY = '{%s}' % ONTOLOGY_NAMESPACE
NSMAP = {'rdf': RDF_NAMESPACE, 'rdfs': RDFS_NAMESPACE, 'ontology': ONTOLOGY_NAMESPACE}

root_element = etree.Element(RDF + 'RDF', nsmap=NSMAP)

parser = etree.XMLParser(remove_blank_text=True)

common = etree.parse('astronomical_database/data/rdf/common.rdf', parser)
for path in [".//rdf:Description"]:
    for element in common.getroot().findall(path, namespaces={'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}):
        root_element.append(element)

astronomy = etree.parse('astronomical_database/data/rdf/astronomy.rdf', parser)
for path in [".//rdf:Description"]:
    for element in astronomy.getroot().findall(path, namespaces={'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}):
        root_element.append(element)

number_of_terrestrial_planets = 0
number_of_gas_giants = 0

for planet in Planet.objects.all():
    rdf_description = etree.SubElement(root_element, RDF + 'Description')
    rdf_description.attrib[RDF + 'about'] = \
        ONTOLOGY_NAMESPACE + 'astronomical_database/individuals/' + planet.name.replace(' ', '_')
    rdf_type = etree.SubElement(rdf_description, RDF + 'type')
    if planet.classification == 'Terrestrial planet':
        number_of_terrestrial_planets += 1
        rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'astronomical_database/astronomy/Terrestrial_Planet'
    elif planet.classification == 'Gas giant':
        number_of_gas_giants += 1
        rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'astronomical_database/astronomy/Gas_Giant'
    else:
        rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'astronomical_database/astronomy/Exoplanet'
    rdfs_label = etree.SubElement(rdf_description, RDFS + 'label')
    rdfs_label.text = planet.name
    if planet.system.host_distance_ly:
        ontology_distance = etree.SubElement(rdf_description, ONTOLOGY + 'distance')
        ontology_distance.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_distance.text = str(planet.system.host_distance_ly) + ' ' + 'ly'
    if planet.radius:
        ontology_size = etree.SubElement(rdf_description, ONTOLOGY + 'size')
        ontology_size.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_size.text = str(planet.radius) + ' ' + 'R<sub>♃</sub>'
    if planet.mass:
        ontology_mass = etree.SubElement(rdf_description, ONTOLOGY + 'mass')
        ontology_mass.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_mass.text = str(planet.mass) + ' ' + 'M<sub>♃</sub>'
    if planet.density:
        ontology_density = etree.SubElement(rdf_description, ONTOLOGY + 'density')
        ontology_density.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_density.text = str(planet.density) + ' ' + 'g/cm³'
    if planet.semimajoraxis:
        ontology_semimajoraxis = etree.SubElement(rdf_description, ONTOLOGY + 'semimajoraxis')
        ontology_semimajoraxis.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_semimajoraxis.text = str(planet.semimajoraxis) + ' ' + 'AU'

for planetarySystem in PlanetarySystem.objects.all():
    rdf_description = etree.SubElement(root_element, RDF + 'Description')
    rdf_description.attrib[RDF + 'about'] = \
        ONTOLOGY_NAMESPACE + 'astronomical_database/individuals/' + planetarySystem.name.replace(' ', '_')
    rdf_type = etree.SubElement(rdf_description, RDF + 'type')
    rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'astronomical_database/astronomy/Planetary_System'
    rdfs_label = etree.SubElement(rdf_description, RDFS + 'label')
    rdfs_label.text = planetarySystem.name
    if planetarySystem.host_distance_ly:
        ontology_distance = etree.SubElement(rdf_description, ONTOLOGY + 'distance')
        ontology_distance.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_distance.text = str(planetarySystem.host_distance_ly) + ' ' + 'ly'
    if planetarySystem.number_of_planets:
        ontology_numberofplanets = etree.SubElement(rdf_description, ONTOLOGY + 'distance')
        ontology_numberofplanets.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_numberofplanets.text = str(planetarySystem.number_of_planets)
    if planetarySystem.max_planet_semimajoraxis and planetarySystem.max_planet_semimajoraxis != 1.:
        ontology_size = etree.SubElement(rdf_description, ONTOLOGY + 'size')
        ontology_size.attrib[RDF + 'datatype'] = FLOAT_NAMESPACE
        ontology_size.text = str(planetarySystem.max_planet_semimajoraxis) + ' ' + 'AU'

number_of_planets = Planet.objects.all().count()
number_of_planetary_systems = PlanetarySystem.objects.all().count()
insert_number_of_instances(root_element, 'astronomy', 'Planet', number_of_planets)
insert_number_of_instances(root_element, 'astronomy', 'Terrestrial_Planet', number_of_terrestrial_planets)
insert_number_of_instances(root_element, 'astronomy', 'Gas_Giant', number_of_gas_giants)
insert_number_of_instances(root_element, 'astronomy', 'Planetary_System', number_of_planetary_systems)
insert_number_of_instances(
    root_element, 'astronomy', 'Astronomical_Object', number_of_planets + number_of_planetary_systems
)
insert_number_of_instances(root_element, 'astronomy', 'Exoplanet', number_of_planets - 8)
insert_number_of_instances(root_element, 'common', 'Thing', number_of_planets + number_of_planetary_systems)

etree.ElementTree(root_element).write(file_name, pretty_print=True)
rdf_file.close()

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
