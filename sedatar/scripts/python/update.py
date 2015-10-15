from sedatar.models import *

import csv

with open('sedatar/data/csv/news/news.csv') as csvfile:

    reader = csv.DictReader(csvfile, skipinitialspace = True, escapechar = '"')

    for row in reader:

        post = Post(name = row['Date'],
                    author = row['Author'],
                    date = row['Date'],
                    headline = row['Headline'],
                    content_left = row['Content_Left'],
                    content_right = row['Content_Right'])
        post.save()

with open('sedatar/data/csv/databases/databases.csv') as csvfile:

    reader = csv.DictReader(csvfile, skipinitialspace = True, escapechar = '"')

    for row in reader:

        database = Database(name = row['Name'],
                            image = row['Image'])
        database.save()
