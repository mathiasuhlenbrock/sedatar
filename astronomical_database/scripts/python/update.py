import csv
import re
from astronomical_database.models import *

def SortIntoCatalogue(cataloguename, row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period):

    from astronomical_database.models import Catalogue, PlanetarySystem

    catalogue = Catalogue.objects.get(name = cataloguename)

    if not PlanetarySystem.objects.filter(name = row['pl_hostname']).exists():

        host_distance = 0.0
        if row['st_dist'] is not "":
            host_distance = row['st_dist']

        host_radius = 0.0
        if row['st_rad'] is not "":
            host_radius = row['st_rad']

        host_spectral_class = "Not available"
        if row['st_spstr'] is not "":
            host_spectral_class = row['st_spstr']

        host_luminosity = 0.0
        if row['st_lum'] is not "":
            host_luminosity = float(row['st_lum'])

        host_BminusV = 0.0
        if row['st_bmvj'] is not "":
            host_BminusV = float(row['st_bmvj'])

        catalogue.planetarysystem_set.create(name = row['pl_hostname'],
                                             host_distance = host_distance,
                                             host_radius = host_radius,
                                             host_spectral_class = host_spectral_class,
                                             host_luminosity = host_luminosity,
                                             host_BminusV = host_BminusV)

    system = PlanetarySystem.objects.get(name = row['pl_hostname'])

    if row["pl_letter"] is not "":
        system.planet_set.create(name = row['pl_hostname'] + " " + row["pl_letter"],
                                 year_of_discovery = year_of_discovery,
                                 density = density,
                                 mass = mass,
                                 radius = radius,
                                 semimajoraxis = semimajoraxis,
                                 orbital_period = orbital_period)

    elif row['pl_name'] is not "":
        system.planet_set.create(name = row['pl_name'],
                                 year_of_discovery = year_of_discovery,
                                 density = density,
                                 mass = mass,
                                 radius = radius,
                                 semimajoraxis = semimajoraxis,
                                 orbital_period = orbital_period)

with open('astronomical_database/data/csv/catalogues/catalogues.csv') as csvfile:

    if Catalogue.objects.exists():

        for catalogue in Catalogue.objects.all():
            catalogue.delete()

    reader = csv.DictReader(csvfile, skipinitialspace = True)

    for row in reader:

        catalogue = Catalogue(name = row['Catalogue'], acronym = row['Acronym'])
        catalogue.save()

with open('astronomical_database/data/csv/categories/categories.csv') as csvfile:

    if Category.objects.exists():

        for category in Category.objects.all():
            category.delete()

    reader = csv.DictReader(csvfile, skipinitialspace = True)

    for row in reader:

        category = Category(name = row['Category'], link = row['Link'])
        category.save()

with open('astronomical_database/data/csv/planets/solar_system.csv') as csvfile:

    if Planet.objects.exists():

        for planet in Planet.objects.all():
            planet.delete()

    if PlanetarySystem.objects.exists():

        for planetarySystem in PlanetarySystem.objects.all():
            planetarySystem.delete()

    reader = csv.DictReader(csvfile, skipinitialspace = True)

    for row in reader:

        year_of_discovery = ""
        if row['pl_disc'] is not "":
            year_of_discovery = row['pl_disc']

        density = 0.0
        if row['pl_dens'] is not "":
            density = float(row['pl_dens'])

        mass = 0.0
        if row['pl_massj'] is not "":
            mass = float(row['pl_massj'])

        radius = 0.0
        if row['pl_radj'] is not "":
            radius = float(row['pl_radj'])

        semimajoraxis = 0.0
        if row['pl_orbsmax'] is not "":
            semimajoraxis = float(row['pl_orbsmax'])

        orbital_period = 0.0
        if row['pl_orbper'] is not "":
            orbital_period = float(row['pl_orbper'])

        SortIntoCatalogue("Stars with proper names", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

with open('astronomical_database/data/csv/planets/planets.csv') as csvfile:

    reader = csv.DictReader(csvfile, skipinitialspace = True)

    for row in reader:

        year_of_discovery = ""
        if row['pl_disc'] is not "":
            year_of_discovery = row['pl_disc']

        density = 0.0
        if row['pl_dens'] is not "":
            density = float(row['pl_dens'])

        mass = 0.0
        if row['pl_massj'] is not "":
            mass = float(row['pl_massj'])

        radius = 0.0
        if row['pl_radj'] is not "":
            radius = float(row['pl_radj'])

        semimajoraxis = 0.0
        if row['pl_orbsmax'] is not "":
            semimajoraxis = float(row['pl_orbsmax'])

        orbital_period = 0.0
        if row['pl_orbper'] is not "":
            orbital_period = float(row['pl_orbper'])

        if re.match("[0-9]?[0-9][ ]", row['pl_hostname']):
            SortIntoCatalogue("Flamsteed designation", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif re.match("HR [0-9]?[0-9]?[0-9]?[0-9]", row['pl_hostname']):
            SortIntoCatalogue("Harvard Revised Catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif re.match("[A-Z][A-Z] [^0-9]+", row['pl_hostname']) or re.match("V[0-9][0-9][0-9]", row['pl_hostname']):
            SortIntoCatalogue("General Catalog of Variable Stars", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif re.match("[a-z]?[a-z][a-z] ", row['pl_hostname']):
            SortIntoCatalogue("Bayer designation", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("1RXS"):
            SortIntoCatalogue("1st ROSAT X-ray Survey", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("2MASS"):
            SortIntoCatalogue("Two Micron All Sky Survey", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("BD"):
            SortIntoCatalogue("Bonner Durchmusterung", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("CHXR"):
            SortIntoCatalogue("Chamaeleon X-ray source ROSAT satellite", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("DENIS-P"):
            SortIntoCatalogue("Deep Near Infrared Survey Provisory designation", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("CoRoT"):
            SortIntoCatalogue("CoRoT Catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("GJ"):
            SortIntoCatalogue("Gliese-Jahreiss catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("GSC"):
            SortIntoCatalogue("Guide Star Catalog", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("HAT"):
            SortIntoCatalogue("Hungarian Automated Telescope", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("HD"):
            SortIntoCatalogue("Henry Draper Catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("HIP"):
            SortIntoCatalogue("Hipparcos Catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("K2"):
            SortIntoCatalogue("K2 Variable Star Catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("KIC"):
            SortIntoCatalogue("Kepler Input Catalog", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("KELT"):
            SortIntoCatalogue("Kilodegree Extremely Little Telescope", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("KOI"):
            SortIntoCatalogue("Kepler Object of Interest", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif "Kepler" in row['pl_hostname']:
            SortIntoCatalogue("Kepler catalog", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("MOA"):
            SortIntoCatalogue("Microlensing Observations in Astrophysics", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("NGC"):
            SortIntoCatalogue("New General Catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("OGLE"):
            SortIntoCatalogue("Optical Gravitational Lensing Experiment", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("POTS"):
            SortIntoCatalogue("Pre-OmegaTranS project", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("Qatar"):
            SortIntoCatalogue("Qatar Exoplanet Survey", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("ROXs"):
            SortIntoCatalogue("Rho Oph X-ray source", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("SWEEPS"):
            SortIntoCatalogue("Sagittarius Window Eclipsing Extrasolar Planet Search", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("TrES"):
            SortIntoCatalogue("Trans-Atlantic Exoplanet Survey", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("TYC"):
            SortIntoCatalogue("Tycho Catalogue", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("USco"):
            SortIntoCatalogue("Upper Sco Cerro Tololo Inter-american Obs", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("WASP"):
            SortIntoCatalogue("Wide Angle Search for Planets", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("WTS"):
            SortIntoCatalogue("WFCAM Transit Survey", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("XO"):
            SortIntoCatalogue("XO project", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("PSR"):
            SortIntoCatalogue("Parkes Selected Region", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'] == "Fomalhaut" or row['pl_hostname'] == "Kapteyn":
            SortIntoCatalogue("Stars with proper names", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        else:
            SortIntoCatalogue("Other stars", row, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)
