from astronomical_database.models import Catalogue
from astronomical_database.models import Category
from astronomical_database.models import Planet
from astronomical_database.models import PlanetarySystem
from astronomical_database.models import Post

import re

import csv

def SortIntoCatalogue(cataloguename, year_of_discovery, density, mass, radius, semimajoraxis, orbital_period):
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

    reader = csv.DictReader(csvfile, skipinitialspace = True)

    for row in reader:

        catalogue = Catalogue(name = row['Catalogue'], acronym = row['Acronym'])
        catalogue.save()

with open('astronomical_database/data/csv/categories/categories.csv') as csvfile:

    reader = csv.DictReader(csvfile, skipinitialspace = True)

    for row in reader:

        category = Category(name = row['Category'], link = row['Link'])
        category.save()

with open('astronomical_database/data/csv/news/news.csv') as csvfile:

    reader = csv.DictReader(csvfile, skipinitialspace = True, escapechar = '"')

    for row in reader:

        post = Post(name = row['Date'],
                    author = row['Author'],
                    date = row['Date'],
                    headline = row['Headline'],
                    content_left = row['Content_Left'],
                    content_right = row['Content_Right'])
        post.save()

with open('astronomical_database/data/csv/planets/solar_system.csv') as csvfile:

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

        SortIntoCatalogue("Stars with proper names", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

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
            SortIntoCatalogue("Flamsteed designation", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif re.match("HR [0-9]?[0-9]?[0-9]?[0-9]", row['pl_hostname']):
            SortIntoCatalogue("Harvard Revised Catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif re.match("[A-Z][A-Z] [^0-9]+", row['pl_hostname']) or re.match("V[0-9][0-9][0-9]", row['pl_hostname']):
            SortIntoCatalogue("General Catalog of Variable Stars", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif re.match("[a-z]?[a-z][a-z] ", row['pl_hostname']):
            SortIntoCatalogue("Bayer designation", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("1RXS"):
            SortIntoCatalogue("1st ROSAT X-ray Survey", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("2MASS"):
            SortIntoCatalogue("Two Micron All Sky Survey", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("BD"):
            SortIntoCatalogue("Bonner Durchmusterung", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("CHXR"):
            SortIntoCatalogue("Chamaeleon X-ray source ROSAT satellite", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("DENIS-P"):
            SortIntoCatalogue("Deep Near Infrared Survey Provisory designation", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("CoRoT"):
            SortIntoCatalogue("CoRoT Catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("GJ"):
            SortIntoCatalogue("Gliese-Jahreiss catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("GSC"):
            SortIntoCatalogue("Guide Star Catalog", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("HAT"):
            SortIntoCatalogue("Hungarian Automated Telescope", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("HD"):
            SortIntoCatalogue("Henry Draper Catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("HIP"):
            SortIntoCatalogue("Hipparcos Catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("K2"):
            SortIntoCatalogue("K2 Variable Star Catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("KIC"):
            SortIntoCatalogue("Kepler Input Catalog", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("KELT"):
            SortIntoCatalogue("Kilodegree Extremely Little Telescope", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("KOI"):
            SortIntoCatalogue("Kepler Object of Interest", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif "Kepler" in row['pl_hostname']:
            SortIntoCatalogue("Kepler catalog", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("MOA"):
            SortIntoCatalogue("Microlensing Observations in Astrophysics", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("NGC"):
            SortIntoCatalogue("New General Catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("OGLE"):
            SortIntoCatalogue("Optical Gravitational Lensing Experiment", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("POTS"):
            SortIntoCatalogue("Pre-OmegaTranS project", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("Qatar"):
            SortIntoCatalogue("Qatar Exoplanet Survey", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("ROXs"):
            SortIntoCatalogue("Rho Oph X-ray source", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("SWEEPS"):
            SortIntoCatalogue("Sagittarius Window Eclipsing Extrasolar Planet Search", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("TrES"):
            SortIntoCatalogue("Trans-Atlantic Exoplanet Survey", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("TYC"):
            SortIntoCatalogue("Tycho Catalogue", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("USco"):
            SortIntoCatalogue("Upper Sco Cerro Tololo Inter-american Obs", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("WASP"):
            SortIntoCatalogue("Wide Angle Search for Planets", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("WTS"):
            SortIntoCatalogue("WFCAM Transit Survey", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("XO"):
            SortIntoCatalogue("XO project", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'].startswith("PSR"):
            SortIntoCatalogue("Parkes Selected Region", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'] == "Fomalhaut" or row['pl_hostname'] == "Kapteyn":
            SortIntoCatalogue("Stars with proper names", year_of_discovery, density, mass, radius, semimajoraxis, orbital_period)

        elif row['pl_hostname'] == "Fomalhaut" or row['pl_hostname'] == "Kapteyn":
            SortIntoCatalogue("Stars with proper names", density, mass, radius, semimajoraxis)

        else:
            SortIntoCatalogue("Other stars", density, mass, radius, semimajoraxis)
