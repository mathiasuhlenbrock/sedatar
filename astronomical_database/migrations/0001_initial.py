# Generated by Django 2.2.3 on 2019-07-23 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('acronym', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PlanetarySystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('host_distance', models.FloatField(default=0.0)),
                ('host_radius', models.FloatField(default=0.0)),
                ('host_spectral_class', models.CharField(max_length=50)),
                ('host_luminosity', models.FloatField(default=0.0)),
                ('host_bminusv', models.FloatField(default=0.0)),
                ('catalogue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='astronomical_database.Catalogue')),
            ],
        ),
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year_of_discovery', models.CharField(max_length=200)),
                ('mass', models.FloatField(default=0.0)),
                ('radius', models.FloatField(default=0.0)),
                ('density', models.FloatField(default=0.0)),
                ('semimajoraxis', models.FloatField(default=0.0)),
                ('orbital_period', models.FloatField(default=0.0)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='astronomical_database.PlanetarySystem')),
            ],
        ),
    ]
