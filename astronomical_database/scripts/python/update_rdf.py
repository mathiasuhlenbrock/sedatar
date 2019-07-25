import csv
from subprocess import call

with open('astronomical_database/data/csv/planets/planets.csv') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        f = open(
            'astronomical_database/data/rdf/individuals/' + row['pl_hostname'].replace(' ', '_') + '_' +
            row['pl_letter'] + '.rdf', 'w'
        )
        f.write(
            '<rdf:Description rdf:about="urn://sedatar.org/astronomical_database/individuals/' +
            row['pl_hostname'].replace(' ', '_') + '_' + row['pl_letter'] + '">\n')
        f.write('  <rdf:type rdf:resource="urn://sedatar.org/astronomical_database/astronomy/Exoplanet" />\n')
        f.write('  <rdfs:label>' + row['pl_hostname'].replace('-', ' ') + ' ' + row['pl_letter'] + '</rdfs:label>\n')
        f.write('  <ontology:distance>' + row['st_dist'] + '</ontology:distance>\n')
        f.write('  <ontology:size>' + row['pl_radj'] + '</ontology:size>\n')
        f.write('  <ontology:mass>' + row['pl_massj'] + '</ontology:mass>\n')
        f.write('  <ontology:density>' + row['pl_dens'] + '</ontology:density>\n')
        f.write('  <ontology:semimajoraxis>' + row['pl_orbsmax'] + '</ontology:semimajoraxis>\n')
        f.write('</rdf:Description>')
        f.close()

call(['astronomical_database/scripts/shell/update_astronomical_database_rdf.sh'])
