import csv
from sedatar.models import *

with open('sedatar/data/csv/news/news.csv') as csvfile:
    if Post.objects.exists():
        for post in Post.objects.all():
            post.delete()
    reader = csv.DictReader(csvfile, skipinitialspace=True, escapechar='"')
    for row in reader:
        post = Post(name=row['Date'],
                    author=row['Author'],
                    date=row['Date'],
                    headline=row['Headline'],
                    content_left=row['Content_Left'],
                    content_right=row['Content_Right'])
        post.save()

with open('sedatar/data/csv/databases/databases.csv') as csvfile:
    if Database.objects.exists():
        for database in Database.objects.all():
            database.delete()
    reader = csv.DictReader(csvfile, skipinitialspace=True, escapechar='"')
    for row in reader:
        database = Database(name=row['Name'],
                            image=row['Image'])
        database.save()
