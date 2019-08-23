import csv
import re
from astronomical_database.models import *


def sort_into_catalogue(cataloguename, row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period):
    from astronomical_database.models import Catalogue, PlanetarySystem
    the_catalogue = Catalogue.objects.get(name=cataloguename)
    if not PlanetarySystem.objects.filter(name=row['pl_hostname']).exists():
        host_distance = 0.0
        if row['st_dist'] is not '':
            host_distance = row['st_dist']
        host_radius = 0.0
        if row['st_rad'] is not '':
            host_radius = row['st_rad']
        host_spectral_class = 'Not available'
        if row['st_spstr'] is not '':
            host_spectral_class = row['st_spstr']
        host_luminosity = 0.0
        if row['st_lum'] is not '':
            host_luminosity = float(row['st_lum'])
        host_bminusv = 0.0
        if row['st_bmvj'] is not '':
            host_bminusv = float(row['st_bmvj'])
        the_catalogue.planetarysystem_set.create(
            name=row['pl_hostname'],
            host_distance=host_distance,
            host_radius=host_radius,
            host_spectral_class=host_spectral_class,
            host_luminosity=host_luminosity,
            host_bminusv=host_bminusv
        )
    system = PlanetarySystem.objects.get(name=row['pl_hostname'])
    if row['pl_letter'] is not '':
        system.planet_set.create(
            name=row['pl_hostname'] + ' ' + row['pl_letter'],
            year_of_discovery=year_of_discovery,
            density=density,
            mass=mass,
            radius=radius,
            semimajoraxis=semimajoraxis,
            orbital_period=orbital_period
        )
    elif row['pl_name'] is not '':
        system.planet_set.create(
            name=row['pl_name'],
            year_of_discovery=year_of_discovery,
            density=density,
            mass=mass,
            radius=radius,
            semimajoraxis=semimajoraxis,
            orbital_period=orbital_period
        )


with open('astronomical_database/data/csv/catalogues/catalogues.csv') as csvfile:
    if Catalogue.objects.exists():
        for catalogue in Catalogue.objects.all():
            catalogue.delete()
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        catalogue = Catalogue(name=row['Catalogue'], acronym=row['Acronym'])
        catalogue.save()

with open('astronomical_database/data/csv/categories/categories.csv') as csvfile:
    if Category.objects.exists():
        for category in Category.objects.all():
            category.delete()
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        category = Category(name=row['Category'], link=row['Link'])
        category.save()

with open('astronomical_database/data/csv/planets/solar_system.csv') as csvfile:
    if Planet.objects.exists():
        for planet in Planet.objects.all():
            planet.delete()
    if PlanetarySystem.objects.exists():
        for planetarySystem in PlanetarySystem.objects.all():
            planetarySystem.delete()
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        year_of_discovery = ''
        if row['pl_disc'] is not '':
            year_of_discovery = row['pl_disc']
        density = 0.0
        if row['pl_dens'] is not '':
            density = float(row['pl_dens'])
        mass = 0.0
        if row['pl_massj'] is not '':
            mass = float(row['pl_massj'])
        radius = 0.0
        if row['pl_radj'] is not '':
            radius = float(row['pl_radj'])
        semimajoraxis = 0.0
        if row['pl_orbsmax'] is not '':
            semimajoraxis = float(row['pl_orbsmax'])
        orbital_period = 0.0
        if row['pl_orbper'] is not '':
            orbital_period = float(row['pl_orbper'])
        sort_into_catalogue(
            'Stars with proper names', row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
        )

with open('astronomical_database/data/csv/planets/planets.csv') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        year_of_discovery = ''
        if row['pl_disc'] is not '':
            year_of_discovery = row['pl_disc']
        density = 0.0
        if row['pl_dens'] is not '':
            density = float(row['pl_dens'])
        mass = 0.0
        if row['pl_massj'] is not '':
            mass = float(row['pl_massj'])
        radius = 0.0
        if row['pl_radj'] is not '':
            radius = float(row['pl_radj'])
        semimajoraxis = 0.0
        if row['pl_orbsmax'] is not '':
            semimajoraxis = float(row['pl_orbsmax'])
        orbital_period = 0.0
        if row['pl_orbper'] is not '':
            orbital_period = float(row['pl_orbper'])
        if row['pl_hostname'].startswith('1RXS'):
            sort_into_catalogue(
                '1st ROSAT X-ray Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif re.match('[a-z]?[a-z][a-z] ', row['pl_hostname']):
            sort_into_catalogue(
                'Bayer designation',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('BD'):
            sort_into_catalogue(
                'Bonner Durchmusterung',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('CFBDSIR'):
            sort_into_catalogue(
                'Canada-France Brown Dwarf Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('Wolf'):
            sort_into_catalogue(
                'Catalogue of High Proper Motion Stars',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('CHXR'):
            sort_into_catalogue(
                'Chamaeleon X-ray source ROSAT satellite',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('CoRoT'):
            sort_into_catalogue(
                'CoRoT Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('DENIS-P'):
            sort_into_catalogue(
                'Deep Near Infrared Survey Provisory designation',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('EPIC'):
            sort_into_catalogue(
                'Ecliptic Plane Input Catalog',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif re.match('[0-9]?[0-9][ ]', row['pl_hostname']):
            sort_into_catalogue(
                'Flamsteed designation',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif re.match('[A-Z][A-Z] [^0-9]+', row['pl_hostname']) or re.match('V[0-9][0-9][0-9]', row['pl_hostname']):
            sort_into_catalogue(
                'General Catalog of Variable Stars',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('GJ') or row['pl_hostname'].startswith('Gl'):
            sort_into_catalogue(
                'Gliese-Jahreiss catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('GSC'):
            sort_into_catalogue(
                'Guide Star Catalog',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif re.match('HR [0-9]?[0-9]?[0-9]?[0-9]', row['pl_hostname']):
            sort_into_catalogue(
                'Harvard Revised Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('HD'):
            sort_into_catalogue(
                'Henry Draper Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('HIP'):
            sort_into_catalogue(
                'Hipparcos Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('HAT'):
            sort_into_catalogue(
                'Hungarian Automated Telescope',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('IC'):
            sort_into_catalogue(
                'Index Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('K2'):
            sort_into_catalogue(
                'K2 Variable Star Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('KIC'):
            sort_into_catalogue(
                'Kepler Input Catalog',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('KOI'):
            sort_into_catalogue(
                'Kepler Object of Interest',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif 'Kepler' in row['pl_hostname']:
            sort_into_catalogue(
                'Kepler catalog',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('KELT'):
            sort_into_catalogue(
                'Kilodegree Extremely Little Telescope',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('KMT'):
            sort_into_catalogue(
                'Korea Microlensing Telescope Network',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('KPS'):
            sort_into_catalogue(
                'Kourovka Planet Search',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('Lupus'):
            sort_into_catalogue(
                'Lupus',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('LHS'):
            sort_into_catalogue(
                'Luyten Half-Second catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('L '):
            sort_into_catalogue(
                'Luyten catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('LSPM'):
            sort_into_catalogue(
                'Lépine-Shara Proper Motion catalog',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('MXB'):
            sort_into_catalogue(
                'Massachusetts X-ray Burster',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('MOA'):
            sort_into_catalogue(
                'Microlensing Observations in Astrophysics',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('NGC'):
            sort_into_catalogue(
                'New General Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('NGTS'):
            sort_into_catalogue(
                'Next Generation Transit Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('NSVS'):
            sort_into_catalogue(
                'Northern Sky Variability Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('OGLE'):
            sort_into_catalogue(
                'Optical Gravitational Lensing Experiment',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('PSR'):
            sort_into_catalogue(
                'Parkes Selected Region',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('PDS'):
            sort_into_catalogue(
                'Pico dos Dias survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('PH'):
            sort_into_catalogue(
                'Planet Hunters',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('POTS'):
            sort_into_catalogue(
                'Pre-OmegaTranS project',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('Qatar'):
            sort_into_catalogue(
                'Qatar Exoplanet Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('ROXs'):
            sort_into_catalogue(
                'Rho Oph X-ray source',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('Ross'):
            sort_into_catalogue(
                'Ross Catalogue of New Proper Motion Stars',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('SWEEPS'):
            sort_into_catalogue(
                'Sagittarius Window Eclipsing Extrasolar Planet Search',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('TOI'):
            sort_into_catalogue(
                'TESS Object of Interest',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('TAP'):
            sort_into_catalogue(
                'Taurus Auriga Perseus',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('TrES'):
            sort_into_catalogue(
                'Trans-Atlantic Exoplanet Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('TCP'):
            sort_into_catalogue(
                'Transient Confirmation Page',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('TRAPPIST'):
            sort_into_catalogue(
                'Transiting Planets and Planetesimals Small Telescope',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('2MASS'):
            sort_into_catalogue(
                'Two Micron All Sky Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('TYC'):
            sort_into_catalogue(
                'Tycho Catalogue',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('UKIRT'):
            sort_into_catalogue(
                'United Kingdom Infrared Telescope',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('USco'):
            sort_into_catalogue(
                'Upper Sco Cerro Tololo Inter-american Obs',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('VHS'):
            sort_into_catalogue(
                'VISTA Hemisphere Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('WTS'):
            sort_into_catalogue(
                'WFCAM Transit Survey',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('WASP'):
            sort_into_catalogue(
                'Wide Angle Search for Planets',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('WISE'):
            sort_into_catalogue(
                'Wide-field Infrared Survey Explorer',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'].startswith('XO'):
            sort_into_catalogue(
                'XO project',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        elif row['pl_hostname'] == 'Fomalhaut' \
            or row['pl_hostname'] == 'Kapteyn' \
            or row['pl_hostname'] == 'Proxima Cen' \
            or row['pl_hostname'] == 'Teegarden\'s Star':
            sort_into_catalogue(
                'Stars with proper names',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
        else:
            sort_into_catalogue(
                'Other stars',
                row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period
            )
