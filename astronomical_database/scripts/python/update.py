from astronomical_database.models import Catalogue
from astronomical_database.models import Category
from astronomical_database.models import Planet
from astronomical_database.models import PlanetarySystem
from astronomical_database.models import Post

import re

import csv

def SortIntoCatalogue(cataloguename, density, mass, radius, semimajoraxis):
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
                                 density = density,
                                 mass = mass,
                                 radius = radius,
                                 semimajoraxis = semimajoraxis)
    elif row['pl_name'] is not "":
        system.planet_set.create(name = row['pl_name'],
                                 density = density,
                                 mass = mass,
                                 radius = radius,
                                 semimajoraxis = semimajoraxis)

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

    reader = csv.DictReader(csvfile, skipinitialspace = True)

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

        SortIntoCatalogue("Stars with proper names", density, mass, radius, semimajoraxis)

with open('astronomical_database/data/csv/planets/planets.csv') as csvfile:

    reader = csv.DictReader(csvfile, skipinitialspace = True)

    for row in reader:

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

        if re.match("[0-9]?[0-9][ ]", row['pl_hostname']):
            SortIntoCatalogue("Flamsteed designation", density, mass, radius, semimajoraxis)

        elif re.match("HR [0-9]?[0-9]?[0-9]?[0-9]", row['pl_hostname']):
            SortIntoCatalogue("Harvard Revised Catalogue", density, mass, radius, semimajoraxis)

        elif re.match("[A-Z][A-Z] [^0-9]+", row['pl_hostname']) or re.match("V[0-9][0-9][0-9]", row['pl_hostname']):
            SortIntoCatalogue("General Catalog of Variable Stars", density, mass, radius, semimajoraxis)

        elif re.match("[a-z]?[a-z][a-z] ", row['pl_hostname']):
            SortIntoCatalogue("Bayer designation", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("1RXS"):
            SortIntoCatalogue("1st ROSAT X-ray Survey", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("2MASS"):
            SortIntoCatalogue("Two Micron All Sky Survey", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("BD"):
            SortIntoCatalogue("Bonner Durchmusterung", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("CHXR"):
            SortIntoCatalogue("Chamaeleon X-ray source ROSAT satellite", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("DENIS-P"):
            SortIntoCatalogue("Deep Near Infrared Survey Provisory designation", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("CoRoT"):
            SortIntoCatalogue("CoRoT Catalogue", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("GJ"):
            SortIntoCatalogue("Gliese-Jahreiss catalogue", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("GSC"):
            SortIntoCatalogue("Guide Star Catalog", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("HAT"):
            SortIntoCatalogue("Hungarian Automated Telescope", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("HD"):
            SortIntoCatalogue("Henry Draper Catalogue", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("HIP"):
            SortIntoCatalogue("Hipparcos Catalogue", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("K2"):
            SortIntoCatalogue("K2 Variable Star Catalogue", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("KIC"):
            SortIntoCatalogue("Kepler Input Catalog", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("KELT"):
            SortIntoCatalogue("Kilodegree Extremely Little Telescope", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("KOI"):
            SortIntoCatalogue("Kepler Object of Interest", density, mass, radius, semimajoraxis)

        elif "Kepler" in row['pl_hostname']:
            SortIntoCatalogue("Kepler catalog", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("MOA"):
            SortIntoCatalogue("Microlensing Observations in Astrophysics", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("NGC"):
            SortIntoCatalogue("New General Catalogue", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("OGLE"):
            SortIntoCatalogue("Optical Gravitational Lensing Experiment", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("POTS"):
            SortIntoCatalogue("Pre-OmegaTranS project", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("Qatar"):
            SortIntoCatalogue("Qatar Exoplanet Survey", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("ROXs"):
            SortIntoCatalogue("Rho Oph X-ray source", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("SWEEPS"):
            SortIntoCatalogue("Sagittarius Window Eclipsing Extrasolar Planet Search", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("TrES"):
            SortIntoCatalogue("Trans-Atlantic Exoplanet Survey", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("TYC"):
            SortIntoCatalogue("Tycho Catalogue", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("USco"):
            SortIntoCatalogue("Upper Sco Cerro Tololo Inter-american Obs", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("WASP"):
            SortIntoCatalogue("Wide Angle Search for Planets", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("WTS"):
            SortIntoCatalogue("WFCAM Transit Survey", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("XO"):
            SortIntoCatalogue("XO project", density, mass, radius, semimajoraxis)

        elif row['pl_hostname'].startswith("PSR"):
            SortIntoCatalogue("Parkes Selected Region", density, mass, radius, semimajoraxis)

        else:
            SortIntoCatalogue("Stars with proper names", density, mass, radius, semimajoraxis)
