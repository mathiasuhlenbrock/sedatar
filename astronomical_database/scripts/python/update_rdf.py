"""
Documentation goes here.
"""

# import rdflib
from lxml import etree

from astronomical_database.models import Catalogue, Planet, PlanetarySystem


def insert(root, entity, property, value):
    target_element = root.xpath(
        '//rdf:Description[@rdf:about="urn://sedatar.org/astronomical_database#'
        + entity + '"]/ontology:' + property,
        namespaces={
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'ontology': 'urn://sedatar.org/astronomical_database#'
        }
    )
    target_element[0].text = str(value)


file_name = 'astronomical_database/data/rdf/astronomical_database.rdf'
rdf_file = open(file_name, 'w')

RDF_NAMESPACE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
RDF_PREFIX = 'rdf'
RDF = '{%s}' % RDF_NAMESPACE
RDFS_NAMESPACE = 'http://www.w3.org/2000/01/rdf-schema#'
RDFS_PREFIX = 'rdfs'
RDFS = '{%s}' % RDFS_NAMESPACE
ONTOLOGY_NAMESPACE = 'urn://sedatar.org/astronomical_database#'
ONTOLOGY_PREFIX = 'ontology'
ONTOLOGY = '{%s}' % ONTOLOGY_NAMESPACE
XSD_NAMESPACE = 'http://www.w3.org/2001/XMLSchema#'
XSD = '{%s}' % XSD_NAMESPACE
XSD_PREFIX = 'xsd'
NSMAP = {
    RDF_PREFIX: RDF_NAMESPACE,
    RDFS_PREFIX: RDFS_NAMESPACE,
    ONTOLOGY_PREFIX: ONTOLOGY_NAMESPACE,
    XSD_PREFIX: XSD_NAMESPACE
}

root_element = etree.Element(RDF + 'RDF', nsmap=NSMAP)

parser = etree.XMLParser(remove_blank_text=True)

number_of_classes = 0

classes = etree.parse('astronomical_database/data/rdf/classes.rdf', parser)
for path in [".//rdf:Description"]:
    for element in classes.getroot().findall(path, namespaces={RDF_PREFIX: RDF_NAMESPACE}):
        root_element.append(element)
        number_of_classes += 1

insert(
    root_element,
    'Class',
    'numberOfInstances',
    number_of_classes
)

properties = etree.parse('astronomical_database/data/rdf/properties.rdf', parser)
for path in [".//rdf:Description"]:
    for element in properties.getroot().findall(path, namespaces={RDF_PREFIX: RDF_NAMESPACE}):
        root_element.append(element)

max_catalogue_size = 0
max_catalogue_size_instance = ''
# TODO: this is not ideal...
min_catalogue_size = 10000
min_catalogue_size_instance = ''
number_of_catalogues = Catalogue.objects.all().count()
sum_catalogue_size = 0.

for catalogue in Catalogue.objects.all():
    rdf_description = etree.SubElement(root_element, RDF + 'Description')
    rdf_description.attrib[RDF + 'about'] = \
        ONTOLOGY_NAMESPACE + catalogue.name.replace(' ', '_')
    rdf_type = etree.SubElement(rdf_description, RDF + 'type')
    rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'Catalogue'
    rdfs_label = etree.SubElement(rdf_description, RDFS + 'label')
    rdfs_label.text = catalogue.name
    if catalogue.number_of_planetary_systems > max_catalogue_size:
        max_catalogue_size = catalogue.number_of_planetary_systems
        max_catalogue_size_instance = catalogue.name
    if catalogue.number_of_planetary_systems < min_catalogue_size:
        min_catalogue_size = catalogue.number_of_planetary_systems
        min_catalogue_size_instance = catalogue.name
    sum_catalogue_size += catalogue.number_of_planetary_systems
    ontology_size = etree.SubElement(rdf_description, ONTOLOGY + 'size')
    ontology_size.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
    ontology_size.text = str(catalogue.number_of_planetary_systems) + ' ' + 'entries'

insert(
    root_element,
    'Catalogue',
    'averageSize',
    str(round(sum_catalogue_size / number_of_catalogues)) + ' ' + 'entries'
)

insert(
    root_element,
    'Catalogue',
    'maxSize',
    str(max_catalogue_size) + ' ' + 'entries'
)

insert(
    root_element,
    'Catalogue',
    'maxSizeInstance',
    max_catalogue_size_instance
)

insert(
    root_element,
    'Catalogue',
    'minSize',
    str(min_catalogue_size) + ' ' + 'entries'
)

insert(
    root_element,
    'Catalogue',
    'minSizeInstance',
    min_catalogue_size_instance
)

insert(
    root_element,
    'Catalogue',
    'numberOfInstances',
    number_of_catalogues
)

number_of_planets_with_density = 0
number_of_planets_with_distance = 0
number_of_planets_with_mass = 0
number_of_planets_with_radius = 0
number_of_terrestrial_planets = 0
number_of_terrestrial_planets_with_density = 0
number_of_terrestrial_planets_with_distance = 0
number_of_terrestrial_planets_with_mass = 0
number_of_terrestrial_planets_with_radius = 0
number_of_gas_giants = 0
number_of_gas_giants_with_density = 0
number_of_gas_giants_with_distance = 0
number_of_gas_giants_with_mass = 0
number_of_gas_giants_with_radius = 0
max_planet_distance = 0
max_planet_distance_instance = ''
max_planet_radius = 0
max_planet_radius_instance = ''
# TODO: this is not ideal...
min_planet_distance = 5000
min_planet_distance_instance = ''
min_planet_radius = Planet.objects.filter(radius__gt=0).first().radius
min_planet_radius_instance = Planet.objects.filter(radius__gt=0).first().name
sum_planet_density = 0
sum_planet_distance = 0
sum_planet_mass = 0
sum_planet_radius = 0
max_terrestrial_planet_distance = 0
max_terrestrial_planet_distance_instance = ''
max_terrestrial_planet_radius = 0
max_terrestrial_planet_radius_instance = ''
# TODO: this is not ideal...
min_terrestrial_planet_distance = 5000
min_terrestrial_planet_distance_instance = ''
min_terrestrial_planet_radius = 1
min_terrestrial_planet_radius_instance = ''
sum_terrestrial_planet_density = 0
sum_terrestrial_planet_distance = 0
sum_terrestrial_planet_mass = 0
sum_terrestrial_planet_radius = 0
max_gas_giant_distance = 0
max_gas_giant_distance_instance = ''
max_gas_giant_radius = 0
max_gas_giant_radius_instance = ''
# TODO: this is not ideal...
min_gas_giant_distance = 5000
min_gas_giant_distance_instance = ''
min_gas_giant_radius = 1
min_gas_giant_radius_instance = ''
sum_gas_giant_density = 0
sum_gas_giant_distance = 0
sum_gas_giant_mass = 0
sum_gas_giant_radius = 0

for planet in Planet.objects.all():
    rdf_description = etree.SubElement(root_element, RDF + 'Description')
    rdf_description.attrib[RDF + 'about'] = \
        ONTOLOGY_NAMESPACE + planet.name.replace(' ', '_')
    rdf_type = etree.SubElement(rdf_description, RDF + 'type')
    if planet.classification == 'Terrestrial planet':
        number_of_terrestrial_planets += 1
        if planet.radius:
            number_of_terrestrial_planets_with_radius += 1
            sum_terrestrial_planet_radius += planet.radius
            if planet.radius > max_terrestrial_planet_radius:
                max_terrestrial_planet_radius = planet.radius
                max_terrestrial_planet_radius_instance = planet.name
            if planet.radius < min_terrestrial_planet_radius:
                min_terrestrial_planet_radius = planet.radius
                min_terrestrial_planet_radius_instance = planet.name
        if planet.system.host_distance_ly:
            number_of_terrestrial_planets_with_distance += 1
            sum_terrestrial_planet_distance += planet.system.host_distance_ly
            if planet.system.host_distance_ly > max_terrestrial_planet_distance:
                max_terrestrial_planet_distance = planet.system.host_distance_ly
                max_terrestrial_planet_distance_instance = planet.name
            if planet.system.host_distance_ly < min_terrestrial_planet_distance:
                min_terrestrial_planet_distance = planet.system.host_distance_ly
                min_terrestrial_planet_distance_instance = planet.name
        if planet.density:
            number_of_terrestrial_planets_with_density += 1
            sum_terrestrial_planet_density += planet.density
        if planet.mass:
            number_of_terrestrial_planets_with_mass += 1
            sum_terrestrial_planet_mass += planet.mass
        rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'Terrestrial_Planet'
    elif planet.classification == 'Gas giant':
        number_of_gas_giants += 1
        if planet.radius:
            number_of_gas_giants_with_radius += 1
            sum_gas_giant_radius += planet.radius
            if planet.radius > max_gas_giant_radius:
                max_gas_giant_radius = planet.radius
                max_gas_giant_radius_instance = planet.name
            if planet.radius < min_gas_giant_radius:
                min_gas_giant_radius = planet.radius
                min_gas_giant_radius_instance = planet.name
        if planet.system.host_distance_ly:
            number_of_gas_giants_with_distance += 1
            sum_gas_giant_distance += planet.system.host_distance_ly
            if planet.system.host_distance_ly > max_gas_giant_distance:
                max_gas_giant_distance = planet.system.host_distance_ly
                max_gas_giant_distance_instance = planet.name
            if planet.system.host_distance_ly < min_gas_giant_distance:
                min_gas_giant_distance = planet.system.host_distance_ly
                min_gas_giant_distance_instance = planet.name
        if planet.density:
            number_of_gas_giants_with_density += 1
            sum_gas_giant_density += planet.density
        if planet.mass:
            number_of_gas_giants_with_mass += 1
            sum_gas_giant_mass += planet.mass
        rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'Gas_Giant'
    else:
        rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'Exoplanet'
    rdfs_label = etree.SubElement(rdf_description, RDFS + 'label')
    rdfs_label.text = planet.name
    if planet.system.host_distance_ly:
        ontology_distance = etree.SubElement(rdf_description, ONTOLOGY + 'distance')
        ontology_distance.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
        if planet.system.host_distance_ly > 1.e-4:
            ontology_distance.text = str(planet.system.host_distance_ly) + ' ' + 'ly'
        else:
            ontology_distance.text = str(round(planet.system.host_distance_ly * 31557600)) + ' ls'
        number_of_planets_with_distance += 1
        sum_planet_distance += planet.system.host_distance_ly
        if planet.system.host_distance_ly > max_planet_distance:
            max_planet_distance = planet.system.host_distance_ly
            max_planet_distance_instance = planet.name
        if planet.system.host_distance_ly < min_planet_distance:
            min_planet_distance = planet.system.host_distance_ly
            min_planet_distance_instance = planet.name
    if planet.radius:
        ontology_radius = etree.SubElement(rdf_description, ONTOLOGY + 'radius')
        ontology_radius.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
        ontology_radius.text = str(planet.radius) + ' ' + 'R<sub>♃</sub>'
        number_of_planets_with_radius += 1
        sum_planet_radius += planet.radius
        if planet.radius > max_planet_radius:
            max_planet_radius = planet.radius
            max_planet_radius_instance = planet.name
        if planet.radius < min_planet_radius:
            min_planet_radius = planet.radius
            min_planet_radius_instance = planet.name
    if planet.mass:
        ontology_mass = etree.SubElement(rdf_description, ONTOLOGY + 'mass')
        ontology_mass.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
        ontology_mass.text = str(planet.mass) + ' ' + 'M<sub>♃</sub>'
        number_of_planets_with_mass += 1
        sum_planet_mass += planet.mass
    if planet.density:
        ontology_density = etree.SubElement(rdf_description, ONTOLOGY + 'density')
        ontology_density.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
        ontology_density.text = str(planet.density) + ' ' + 'g/cm³'
        number_of_planets_with_density += 1
        sum_planet_density += planet.density
    if planet.semimajoraxis:
        ontology_semimajoraxis = etree.SubElement(rdf_description, ONTOLOGY + 'semimajoraxis')
        ontology_semimajoraxis.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
        ontology_semimajoraxis.text = str(planet.semimajoraxis) + ' ' + 'AU'

number_of_planetary_systems_with_distance = 0
number_of_planetary_systems_with_max_semi_major_axis = 0
max_planetary_system_distance = 0
max_planetary_system_distance_instance = ''
max_planetary_system_max_semi_major_axis = 0
max_planetary_system_max_semi_major_axis_instance = ''
min_planetary_system_distance = 5000
min_planetary_system_distance_instance = ''
min_planetary_system_max_semi_major_axis = 30
min_planetary_system_max_semi_major_axis_instance = ''
sum_planetary_system_distance = 0
sum_planetary_system_max_semi_major_axis = 0

for planetarySystem in PlanetarySystem.objects.all():
    rdf_description = etree.SubElement(root_element, RDF + 'Description')
    rdf_description.attrib[RDF + 'about'] = \
        ONTOLOGY_NAMESPACE + planetarySystem.name.replace(' ', '_')
    rdf_type = etree.SubElement(rdf_description, RDF + 'type')
    rdf_type.attrib[RDF + 'resource'] = ONTOLOGY_NAMESPACE + 'Planetary_System'
    rdfs_label = etree.SubElement(rdf_description, RDFS + 'label')
    rdfs_label.text = planetarySystem.name
    if planetarySystem.host_distance_ly:
        ontology_distance = etree.SubElement(rdf_description, ONTOLOGY + 'distance')
        ontology_distance.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
        if planet.system.host_distance_ly > 1.e-4:
            ontology_distance.text = str(planetarySystem.host_distance_ly) + ' ' + 'ly'
        else:
            ontology_distance.text = str(round(planetarySystem.host_distance_ly * 31557600)) + ' ls'
        number_of_planetary_systems_with_distance += 1
        sum_planetary_system_distance += planetarySystem.host_distance_ly
        if planetarySystem.host_distance_ly > max_planetary_system_distance:
            max_planetary_system_distance = planetarySystem.host_distance_ly
            max_planetary_system_distance_instance = planetarySystem.name
        if 1 < planetarySystem.host_distance_ly < min_planetary_system_distance:
            min_planetary_system_distance = planetarySystem.host_distance_ly
            min_planetary_system_distance_instance = planetarySystem.name
    # if planetarySystem.number_of_planets:
    #     ontology_numberofplanets = etree.SubElement(rdf_description, ONTOLOGY + 'distance')
    #     ontology_numberofplanets.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
    #     ontology_numberofplanets.text = str(planetarySystem.number_of_planets)
    if planetarySystem.max_planet_semimajoraxis and planetarySystem.max_planet_semimajoraxis != 1.:
        ontology_max_semimajoraxis = etree.SubElement(rdf_description, ONTOLOGY + 'maxSemiMajorAxis')
        ontology_max_semimajoraxis.attrib[RDF + 'datatype'] = XSD_PREFIX + ':' + 'string'
        ontology_max_semimajoraxis.text = str(planetarySystem.max_planet_semimajoraxis) + ' ' + 'AU'
        number_of_planetary_systems_with_max_semi_major_axis += 1
        sum_planetary_system_max_semi_major_axis += planetarySystem.max_planet_semimajoraxis
        if planetarySystem.max_planet_semimajoraxis > max_planetary_system_max_semi_major_axis:
            max_planetary_system_max_semi_major_axis = planetarySystem.max_planet_semimajoraxis
            max_planetary_system_max_semi_major_axis_instance = planetarySystem.name
        if planetarySystem.max_planet_semimajoraxis < min_planetary_system_max_semi_major_axis:
            min_planetary_system_max_semi_major_axis = planetarySystem.max_planet_semimajoraxis
            min_planetary_system_max_semi_major_axis_instance = planetarySystem.name

number_of_planets = Planet.objects.all().count()
number_of_planetary_systems = PlanetarySystem.objects.all().count()

insert(
    root_element,
    'Planet',
    'averageDensity',
    str(round(sum_planet_density / number_of_planets_with_density, 3)) + ' ' + 'g/cm³'
)
insert(
    root_element,
    'Planet',
    'averageDistance',
    str(round(sum_planet_distance / number_of_planets_with_distance, 3)) + ' ' + 'ly'
)
insert(
    root_element,
    'Planet',
    'averageMass',
    str(round(sum_planet_mass / number_of_planets_with_mass, 3)) + ' ' + 'M<sub>♃</sub>'
)
insert(
    root_element,
    'Planet',
    'averageRadius',
    str(round(sum_planet_radius / number_of_planets_with_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Planet',
    'maxDistanceInstance',
    max_planet_distance_instance
)
insert(
    root_element,
    'Planet',
    'minDistanceInstance',
    min_planet_distance_instance
)
insert(
    root_element,
    'Planet',
    'maxRadius',
    str(round(max_planet_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Planet',
    'maxRadiusInstance',
    max_planet_radius_instance
)
insert(
    root_element,
    'Planet',
    'minRadius',
    str(round(min_planet_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Planet',
    'minRadiusInstance',
    min_planet_radius_instance
)
insert(
    root_element,
    'Planet',
    'numberOfInstances',
    number_of_planets
)
insert(
    root_element,
    'Terrestrial_Planet',
    'averageDensity',
    str(round(sum_terrestrial_planet_density / number_of_terrestrial_planets_with_density, 3)) + ' ' + 'g/cm³'
)
insert(
    root_element,
    'Terrestrial_Planet',
    'averageDistance',
    str(round(sum_terrestrial_planet_distance / number_of_terrestrial_planets_with_distance, 3)) + ' ' + 'ly'
)
insert(
    root_element,
    'Terrestrial_Planet',
    'averageMass',
    str(round(sum_terrestrial_planet_mass / number_of_terrestrial_planets_with_mass, 3)) + ' ' + 'M<sub>♃</sub>'
)
insert(
    root_element,
    'Terrestrial_Planet',
    'averageRadius',
    str(round(sum_terrestrial_planet_radius / number_of_terrestrial_planets_with_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Terrestrial_Planet',
    'maxDistanceInstance',
    max_terrestrial_planet_distance_instance
)
insert(
    root_element,
    'Terrestrial_Planet',
    'minDistanceInstance',
    min_terrestrial_planet_distance_instance
)
insert(
    root_element,
    'Terrestrial_Planet',
    'maxRadius',
    str(round(max_terrestrial_planet_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Terrestrial_Planet',
    'maxRadiusInstance',
    max_terrestrial_planet_radius_instance
)
insert(
    root_element,
    'Terrestrial_Planet',
    'minRadius',
    str(round(min_terrestrial_planet_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Terrestrial_Planet',
    'minRadiusInstance',
    min_terrestrial_planet_radius_instance
)
insert(
    root_element,
    'Terrestrial_Planet',
    'numberOfInstances',
    number_of_terrestrial_planets
)
insert(
    root_element,
    'Gas_Giant',
    'averageDensity',
    str(round(sum_gas_giant_density / number_of_gas_giants_with_density, 3)) + ' ' + 'g/cm³'
)
insert(
    root_element,
    'Gas_Giant',
    'averageDistance',
    str(round(sum_gas_giant_distance / number_of_gas_giants_with_distance, 3)) + ' ' + 'ly'
)
insert(
    root_element,
    'Gas_Giant',
    'averageMass',
    str(round(sum_gas_giant_mass / number_of_gas_giants_with_mass, 3)) + ' ' + 'M<sub>♃</sub>'
)
insert(
    root_element,
    'Gas_Giant',
    'averageRadius',
    str(round(sum_gas_giant_radius / number_of_gas_giants_with_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Gas_Giant',
    'maxDistanceInstance',
    max_gas_giant_distance_instance
)
insert(
    root_element,
    'Gas_Giant',
    'minDistanceInstance',
    min_gas_giant_distance_instance
)
insert(
    root_element,
    'Gas_Giant',
    'maxRadius',
    str(round(max_gas_giant_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Gas_Giant',
    'maxRadiusInstance',
    max_gas_giant_radius_instance
)
insert(
    root_element,
    'Gas_Giant',
    'minRadius',
    str(round(min_gas_giant_radius, 3)) + ' ' + 'R<sub>♃</sub>'
)
insert(
    root_element,
    'Gas_Giant',
    'minRadiusInstance',
    min_gas_giant_radius_instance
)
insert(
    root_element,
    'Gas_Giant',
    'numberOfInstances',
    number_of_gas_giants
)
insert(
    root_element,
    'Planetary_System',
    'averageDistance',
    str(round(sum_planetary_system_distance / number_of_planetary_systems_with_distance, 3)) + ' ' + 'ly'
)
insert(
    root_element,
    'Planetary_System',
    'averageMaxSemiMajorAxis',
    str(
        round(sum_planetary_system_max_semi_major_axis / number_of_planetary_systems_with_max_semi_major_axis, 3)
    ) + ' ' + 'AU'
)
insert(
    root_element,
    'Planetary_System',
    'maxDistanceInstance',
    max_planetary_system_distance_instance
)
insert(
    root_element,
    'Planetary_System',
    'minDistanceInstance',
    min_planetary_system_distance_instance
)
insert(
    root_element,
    'Planetary_System',
    'maxMaxSemiMajorAxis',
    str(round(max_planetary_system_max_semi_major_axis, 3)) + ' ' + 'AU'
)
insert(
    root_element,
    'Planetary_System',
    'maxMaxSemiMajorAxisInstance',
    max_planetary_system_max_semi_major_axis_instance
)
insert(
    root_element,
    'Planetary_System',
    'minMaxSemiMajorAxis',
    str(round(min_planetary_system_max_semi_major_axis, 3)) + ' ' + 'AU'
)
insert(
    root_element,
    'Planetary_System',
    'minMaxSemiMajorAxisInstance',
    min_planetary_system_max_semi_major_axis_instance
)
insert(
    root_element,
    'Planetary_System',
    'numberOfInstances',
    number_of_planetary_systems
)
insert(
    root_element,
    'Astronomical_Object',
    'numberOfInstances',
    number_of_planets + number_of_planetary_systems
)
insert(
    root_element,
    'Exoplanet',
    'numberOfInstances',
    number_of_planets - 8
)
insert(
    root_element,
    'Thing',
    'numberOfInstances',
    number_of_catalogues + number_of_planets + number_of_planetary_systems
)

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
