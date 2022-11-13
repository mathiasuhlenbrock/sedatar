from django.db import models
from astronomical_database.constants import M_EARTH, M_JUPITER, R_EARTH, R_JUPITER


class Catalogue(models.Model):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=200)
    ordering_strategy = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def page_name(self):
        return self.name.replace(' ', '_')

    @property
    def number_of_planetary_systems(self):
        return self.planetarysystem_set.all().count()


class Category(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PlanetarySystem(models.Model):
    name = models.CharField(max_length=200)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)
    host_distance = models.FloatField(default=0.0)
    host_radius = models.FloatField(default=0.0)
    host_spectral_class = models.CharField(max_length=50)
    host_luminosity = models.FloatField(default=0.0)
    host_bminusv = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    @property
    def page_name(self):
        return self.name.replace(' ', '_')

    @property
    def number_of_planets(self):
        return self.planet_set.all().count()

    @property
    def host_classification(self):
        if ' 0' in self.host_spectral_class:
            return 'Hypergiant star'
        elif ' Ia' in self.host_spectral_class or ' Ib' in self.host_spectral_class:
            return 'Supergiant star'
        elif ' II' in self.host_spectral_class:
            return 'Bright giant star'
        elif ' III' in self.host_spectral_class or ' IIIb' in self.host_spectral_class:
            return 'Giant star'
        elif ' IV' in self.host_spectral_class:
            return 'Subgiant star'
        elif ' V' in self.host_spectral_class or ' Vne' in self.host_spectral_class:
            return 'Main sequence star'
        elif ' VI' in self.host_spectral_class:
            return 'Subdwarf star'
        elif self.host_spectral_class.startswith('sdB'):
            return 'Class B subdwarf star'
        elif self.host_spectral_class.startswith('L'):
            return 'Class L brown dwarf star'
        elif self.host_spectral_class.startswith('T'):
            return 'Class T brown dwarf star'
        elif ' VII' in self.host_spectral_class:
            return 'White dwarf star'
        else:
            return 'Classification not available'

    # Auxiliary parameters.

    @property
    def host_distance_ly(self):
        host_distance_ly = self.host_distance * 3.26
        if host_distance_ly < 1:
            return round(host_distance_ly, 8)
        else:
            return round(host_distance_ly)

    @property
    def max_planet_radius(self):
        max_planet_radius = 0.0
        for planet in self.planet_set.all():
            if planet.radius > max_planet_radius:
                max_planet_radius = planet.radius
        if max_planet_radius > 0.0:
            return max_planet_radius
        else:
            return 1.

    @property
    def max_planet_semimajoraxis(self):
        max_planet_semimajoraxis = 0.0
        for planet in self.planet_set.all():
            if planet.semimajoraxis > max_planet_semimajoraxis:
                max_planet_semimajoraxis = planet.semimajoraxis
        if max_planet_semimajoraxis > 0.0:
            return max_planet_semimajoraxis
        else:
            return 1.

    # String representations of system parameters.

    @property
    def string_host_distance_ly(self):
        if self.host_distance_ly > 1.e-4:
            return str(self.host_distance_ly) + ' ly'
        elif self.host_distance_ly > 0.:
            return str(round(self.host_distance_ly * 31557600)) + ' ls'
        else:
            return 'Not available'

    @property
    def string_host_radius(self):
        if self.host_radius > 0.:
            return str(self.host_radius) + ' R<sub>&#9737;</sub>'
        else:
            return 'Not available'

    @property
    def string_host_luminosity(self):
        if self.host_luminosity > 0.:
            return str(self.host_luminosity) + ' Log(L<sub>&#9737;</sub>)'
        else:
            return 'Not available'

    @property
    def string_host_bminusv(self):
        if self.host_bminusv > 0.:
            return str(self.host_bminusv)
        else:
            return 'Not available'

    @property
    def string_max_planet_semimajoraxis(self):
        max_planet_semimajoraxis = 0.0
        for planet in self.planet_set.all():
            if planet.semimajoraxis > max_planet_semimajoraxis:
                max_planet_semimajoraxis = planet.semimajoraxis
        if max_planet_semimajoraxis > 0.0:
            return str(max_planet_semimajoraxis) + ' AU'
        else:
            return 'Not available'

    # Image parameters.

    @property
    def img_host_spectral_class(self):
        if self.host_spectral_class.startswith('O'):
            return 'spectral_class_0'
        elif self.host_spectral_class.startswith('B') or self.host_spectral_class.startswith('sdB'):
            return 'spectral_class_B'
        elif self.host_spectral_class.startswith('A'):
            return 'spectral_class_A'
        elif self.host_spectral_class.startswith('F'):
            return 'spectral_class_F'
        elif self.host_spectral_class.startswith('G'):
            return 'spectral_class_G'
        elif self.host_spectral_class.startswith('K'):
            return 'spectral_class_K'
        elif self.host_spectral_class.startswith('M'):
            return 'spectral_class_M'
        elif self.host_spectral_class.startswith('L'):
            return 'spectral_class_L'
        elif self.host_spectral_class.startswith('T'):
            return 'spectral_class_T'
        elif self.host_spectral_class.startswith('WD'):
            return 'spectral_class_WD'
        else:
            return 'spectral_class_default'

    @property
    def img_host_rel_radius(self):
        min_semimajoraxis = 1.e99
        for planet in self.planet_set.all():
            if planet.semimajoraxis and planet.semimajoraxis < min_semimajoraxis:
                min_semimajoraxis = planet.semimajoraxis
        if min_semimajoraxis < 1.e99:
            return min_semimajoraxis / self.max_planet_semimajoraxis * 100 * 0.5
        else:
            return 50

    @property
    def img_host_rel_inner_radius(self):
        return self.img_host_rel_radius - 2

    @property
    def img_host_radius(self):
        if 1. >= self.host_radius > 0.:
            return round(50 * self.host_radius)
        elif self.host_radius > 1.:
            return 50
        else:
            return 0

    @property
    def img_sun_radius(self):
        if self.host_radius <= 1.:
            return 50
        else:
            return round(50 / self.host_radius)


class Planet(models.Model):
    name = models.CharField(max_length=200)
    system = models.ForeignKey(PlanetarySystem, on_delete=models.CASCADE)
    year_of_discovery = models.CharField(max_length=200)
    mass = models.FloatField(default=0.0)
    radius = models.FloatField(default=0.0)
    density = models.FloatField(default=0.0)
    semimajoraxis = models.FloatField(default=0.0)
    orbital_period = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    @property
    def page_name(self):
        return self.name.replace(' ', '_')

    @property
    def index(self):
        index = 0
        for planet in self.system.planet_set.all().order_by('semimajoraxis'):
            if planet.semimajoraxis:
                index += 1
                if self.name == planet.name:
                    return index

    @property
    def classification(self):
        if self.density <= 0.0:
            return 'no_classification'
        elif self.density < 1.869 or self.radius > 0.35:
            if 0.36 <= self.mass <= 11.8 and 0. < self.orbital_period <= 111.:
                return 'hot_jupiter'
            else:
                return 'gas_giant'
        else:
            return 'terrestrial_planet'

    @property
    def title_classification(self):
        if self.classification == 'gas_giant':
            return 'Gas giant'
        elif self.classification == 'hot_jupiter':
            return 'Hot Jupiter'
        elif self.classification == 'terrestrial_planet':
            return 'Terrestrial planet'
        else:
            return 'No classification available'

    def table_classification(self):
        if self.classification == 'gas_giant':
            return 'gas giant'
        elif self.classification == 'hot_jupiter':
            return 'hot Jupiter'
        elif self.classification == 'terrestrial_planet':
            return 'terrestrial'
        else:
            return 'no classification'

    # Auxiliary parameters.

    @property
    def rel_axis(self):
        return self.semimajoraxis / self.system.max_planet_semimajoraxis

    # String representations of planetary parameters.

    @property
    def string_radius(self):
        if self.radius > 0.:
            if self.classification == 'Terrestrial planet':
                return str(round(self.radius * R_JUPITER / R_EARTH, 3)) + ' R<sub>&#9793</sub>'
            else:
                return str(round(self.radius, 3)) + ' R<sub>&#9795;</sub>'
        else:
            return 'Not available'

    @property
    def string_mass(self):
        if self.mass > 0.:
            if self.classification == 'Terrestrial planet':
                return str(round(self.mass * M_JUPITER / M_EARTH, 3)) + ' M<sub>&#9793</sub>'
            else:
                return str(round(self.mass, 3)) + ' M<sub>&#9795;</sub>'
        else:
            return 'Not available'

    @property
    def string_density(self):
        if self.density > 0.:
            return str(round(self.density, 3)) + ' g/cm&sup3;'
        else:
            return 'Not available'

    @property
    def string_semimajoraxis(self):
        if self.semimajoraxis > 0.:
            return str(round(self.semimajoraxis, 3)) + ' AU'
        else:
            return 'Not available'

    @property
    def string_orbital_period(self):
        if self.orbital_period > 0:
            return str(round(self.orbital_period, 3)) + ' days'
        else:
            return 'Not available'

    # Image parameters.

    @property
    def img_classification(self):
        if self.classification == 'gas_giant':
            return 'gas_giant'
        elif self.classification == 'terrestrial_planet':
            return 'terrestrial'
        else:
            return 'default'

    @property
    def img_radius(self):
        if 0. < self.radius <= 1.:
            return round(50 * self.radius)
        elif self.radius > 1.:
            return 50
        else:
            return 0

    @property
    def img_alt_radius(self):
        if 0 < self.radius * R_JUPITER / R_EARTH <= 1:
            return round(50 * self.radius * R_JUPITER / R_EARTH)
        elif self.radius * R_JUPITER / R_EARTH > 1.:
            return 50
        else:
            return 0

    @property
    def img_earth_radius(self):
        if self.radius * R_JUPITER / R_EARTH <= 1.:
            return 50
        else:
            return round(50 / (self.radius * R_JUPITER / R_EARTH))

    @property
    def img_jupiter_radius(self):
        if self.radius <= 1.:
            return 50
        else:
            return round(50 / self.radius)

    @property
    def img_rel_radius(self):
        if self.radius:
            return self.radius / self.system.max_planet_radius * 10
        else:
            return 10

    @property
    def img_rel_inner_radius(self):
        return self.img_rel_radius - 2

    @property
    def img_rel_semimajoraxis(self):
        return self.rel_axis * 250

    @property
    def img_line1_y1(self):
        if self.index:
            return 253 + (self.index - 1) * 27

    @property
    def img_line2_y1(self):
        return self.img_line1_y1 + 1

    @property
    def img_text_y(self):
        return self.img_line1_y1 - 6

    @property
    def img_legend_x2(self):
        return self.img_rel_semimajoraxis + 260

    @property
    def img_legend_x1(self):
        return self.img_legend_x2 - 60

    @property
    def img_rel_semiminoraxis(self):
        return self.rel_axis * 100

    @property
    def img_cx(self):
        return self.img_rel_semimajoraxis + 260
