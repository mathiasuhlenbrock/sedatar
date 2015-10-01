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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('density', models.FloatField(default=0.0)),
                ('mass', models.FloatField(default=0.0)),
                ('radius', models.FloatField(default=0.0)),
                ('semimajoraxis', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('headline', models.CharField(max_length=200)),
                ('content_left', models.TextField(default=b'')),
                ('content_right', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='planet',
            name='system',
            field=models.ForeignKey(to='astronomical_database.PlanetarySystem'),
            preserve_default=True,
        ),
    ]
