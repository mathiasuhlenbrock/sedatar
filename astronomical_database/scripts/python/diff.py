import csv
import sys 

with open('../../data/csv/planets/planets.09-01-2015.stripped.csv') as csvfile_old:

    reader = csv.DictReader(csvfile_old,skipinitialspace=True)

    planetlist_old = []

    for row in reader:

        planetlist_old.append(row['pl_hostname'] + " " + row['pl_letter'])

    csvfile_new = open('../../data/csv/planets/planets.10-01-2015.stripped.csv')

    reader = csv.DictReader(csvfile_new,skipinitialspace=True)

    sys.stdout.write("<table><tr><td class=\"cell_standard\">")

    counter = 1

    for row in reader:

        planetFound = False 
        planet = row['pl_hostname'] + " " + row['pl_letter']

        for entry in planetlist_old:

            if entry == planet:

                planetFound = True
                break

        if not planetFound:

            sys.stdout.write(planet + "</td></tr><tr><td class=\"cell_standard\">")

            if (counter % 20 == 0):

                sys.stdout.write("</td></tr></table><table><tr><td class=\"cell_standard\">")

            counter += 1

    sys.stdout.write("</td></tr></table>")
