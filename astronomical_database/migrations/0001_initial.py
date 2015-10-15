# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('acronym', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('year_of_discovery', models.CharField(max_length=200)),
                ('mass', models.FloatField(default=0.0)),
                ('radius', models.FloatField(default=0.0)),
                ('density', models.FloatField(default=0.0)),
                ('semimajoraxis', models.FloatField(default=0.0)),
                ('orbital_period', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='PlanetarySystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('host_distance', models.FloatField(default=0.0)),
                ('host_radius', models.FloatField(default=0.0)),
                ('host_spectral_class', models.CharField(max_length=50)),
                ('host_luminosity', models.FloatField(default=0.0)),
                ('host_BminusV', models.FloatField(default=0.0)),
                ('catalogue', models.ForeignKey(to='astronomical_database.Catalogue')),
            ],
        ),
        migrations.AddField(
            model_name='planet',
            name='system',
            field=models.ForeignKey(to='astronomical_database.PlanetarySystem'),
        ),
    ]
