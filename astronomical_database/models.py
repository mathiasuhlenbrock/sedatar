from django.db import models

# Create your models here.

class Catalogue(models.Model):
    name     = models.CharField(max_length = 200)
    acronym  = models.CharField(max_length = 200)

    def __unicode__(self):
       return self.name

    def _get_page_name(self):
        return self.name.replace(" ", "_")

    page_name = property(_get_page_name)

    def _get_number_of_planetary_systems(self):
        return self.planetarysystem_set.all().count()

    number_of_planetary_systems = property(_get_number_of_planetary_systems)

class Category(models.Model):
    name = models.CharField(max_length = 200)
    link = models.CharField(max_length = 200)

    def __unicode__(self):
       return self.name

class PlanetarySystem(models.Model):
    name                = models.CharField(max_length = 200)
    catalogue           = models.ForeignKey(Catalogue)
    host_distance       = models.FloatField(default = 0.0)
    host_radius         = models.FloatField(default = 0.0)
    host_spectral_class = models.CharField(max_length = 50)
    host_luminosity     = models.FloatField(default = 0.0)
    host_BminusV        = models.FloatField(default = 0.0)

    def __unicode__(self):
       return self.name

    def _get_page_name(self):
        return self.name.replace(" ", "_")

    page_name = property(_get_page_name)

    def _get_catalogue_page_name(self):
        return str(self.catalogue).replace(" ", "_")

    catalogue_page_name = property(_get_catalogue_page_name)

    def _get_number_of_planets(self):
        return self.planet_set.all().count()

    number_of_planets = property(_get_number_of_planets)

    def _get_host_classification(self):
        if " 0" in self.host_spectral_class:
            return "Hypergiant star"
        elif " Ia" in self.host_spectral_class or " Ib" in self.host_spectral_class:
            return "Supergiant star"
        elif " II" in self.host_spectral_class:
            return "Bright giant star"
        elif " III" in self.host_spectral_class or " IIIb" in self.host_spectral_class:
            return "Giant star"
        elif " IV" in self.host_spectral_class:
            return "Subgiant star"
        elif " V" in self.host_spectral_class or " Vne" in self.host_spectral_class:
            return "Main sequence star"
        elif " VI" in self.host_spectral_class:
            return "Subdwarf star"
        elif self.host_spectral_class.startswith("sdB"):
            return "Class B subdwarf star"
        elif self.host_spectral_class.startswith("L"):
            return "Class L brown dwarf star"
        elif self.host_spectral_class.startswith("T"):
            return "Class T brown dwarf star"
        elif " VII" in self.host_spectral_class:
            return "White dwarf star"
        else:
            return "Classification not available"

    host_classification = property(_get_host_classification)

    # Auxilliary parameters.

    def _get_host_distance_ly(self):
        return round(self.host_distance * 3.26)

    host_distance_ly = property(_get_host_distance_ly)

    def _get_max_planet_radius(self):
        max_planet_radius = 0.0

        for planet in self.planet_set.all():
            if planet.radius > max_planet_radius:
                max_planet_radius = planet.radius

        if max_planet_radius > 0.0:
            return max_planet_radius
        else:
            return 1.

    max_planet_radius = property(_get_max_planet_radius)

    def _get_max_planet_semimajoraxis(self):
        max_planet_semimajoraxis = 0.0

        for planet in self.planet_set.all():
            if planet.semimajoraxis > max_planet_semimajoraxis:
                max_planet_semimajoraxis = planet.semimajoraxis

        if max_planet_semimajoraxis > 0.0:
            return max_planet_semimajoraxis
        else:
            return 1.

    max_planet_semimajoraxis = property(_get_max_planet_semimajoraxis)

    # String representations of system parameters.

    def _get_string_host_radius(self):
        if self.host_radius > 0.:
            return str(self.host_radius) + " R<sub>&#9737;</sub>"
        else:
            return "Not available"

    string_host_radius = property(_get_string_host_radius)

    def _get_string_host_luminosity(self):
        if self.host_luminosity > 0.:
            return str(self.host_luminosity) + " Log(L<sub>&#9737;</sub>)"
        else:
            return "Not available"

    string_host_luminosity = property(_get_string_host_luminosity)

    def _get_string_host_BminusV(self):
        if self.host_BminusV > 0.:
            return str(self.host_BminusV)
        else:
            return "Not available"

    string_host_BminusV = property(_get_string_host_BminusV)

    def _get_string_max_planet_semimajoraxis(self):
        max_planet_semimajoraxis = 0.0

        for planet in self.planet_set.all():
            if planet.semimajoraxis > max_planet_semimajoraxis:
                max_planet_semimajoraxis = planet.semimajoraxis

        if max_planet_semimajoraxis > 0.0:
            return str(max_planet_semimajoraxis) + " AU"
        else:
            return "Not available"

    string_max_planet_semimajoraxis = property(_get_string_max_planet_semimajoraxis)

    # Image parameters.

    def _get_img_host_spectral_class(self):
        if self.host_spectral_class.startswith("O"):
            return "spectral_class_0"
        elif self.host_spectral_class.startswith("B") or self.host_spectral_class.startswith("sdB"):
            return "spectral_class_B"
        elif self.host_spectral_class.startswith("A"):
            return "spectral_class_A"
        elif self.host_spectral_class.startswith("F"):
            return "spectral_class_F"
        elif self.host_spectral_class.startswith("G"):
            return "spectral_class_G"
        elif self.host_spectral_class.startswith("K"):
            return "spectral_class_K"
        elif self.host_spectral_class.startswith("M"):
            return "spectral_class_M"
        elif self.host_spectral_class.startswith("L"):
            return "spectral_class_L"
        elif self.host_spectral_class.startswith("T"):
            return "spectral_class_T"
        elif self.host_spectral_class.startswith("WD"):
            return "spectral_class_WD"
        else:
            return "spectral_class_default"

    img_host_spectral_class = property(_get_img_host_spectral_class)

    def _get_img_host_rel_radius(self):
        min_semimajoraxis = 1.e99

        for planet in self.planet_set.all():
            if planet.semimajoraxis and planet.semimajoraxis < min_semimajoraxis:
                min_semimajoraxis = planet.semimajoraxis

        if min_semimajoraxis < 1.e99:
            return min_semimajoraxis / self.max_planet_semimajoraxis * 100 * 0.5
        else:
            return 50

    img_host_rel_radius = property(_get_img_host_rel_radius)

    def _get_img_host_rel_inner_radius(self):
       return self.img_host_rel_radius - 2 

    img_host_rel_inner_radius = property(_get_img_host_rel_inner_radius)

    def _get_img_host_radius(self):
        if self.host_radius <= 1. and self.host_radius > 0.:
            return round(50 * self.host_radius)
        elif self.host_radius > 1.:
            return 50
        else:
            return 0

    img_host_radius = property(_get_img_host_radius)

    def _get_img_sun_radius(self):
        if self.host_radius <= 1.:
            return 50
        else:
            return round(50 / self.host_radius)

    img_sun_radius = property(_get_img_sun_radius)

class Post(models.Model):
    name          = models.CharField(max_length = 200)
    author        = models.CharField(max_length = 200)
    date          = models.DateField()
    headline      = models.CharField(max_length = 200)
    content_left  = models.TextField(default = "")
    content_right = models.TextField(default = "", blank = True)

    def __unicode__(self):
       return self.name

class Planet(models.Model):
    name          = models.CharField(max_length = 200)
    system        = models.ForeignKey(PlanetarySystem)
    density       = models.FloatField(default = 0.0)
    mass          = models.FloatField(default = 0.0)
    radius        = models.FloatField(default = 0.0)
    semimajoraxis = models.FloatField(default = 0.0)
 
    def __unicode__(self):
       return self.name

    def _get_index(self):
        index = 0

        for planet in self.system.planet_set.all().order_by('semimajoraxis'):
            if planet.semimajoraxis:
                index += 1
                if self.name == planet.name:
                    return index

    index = property(_get_index)

    def _get_classification(self):
        if self.density <= 0.0:
            return "default"
        elif self.density < 1.869 or self.radius > 0.35:
            return "gas_giant"
        else:
            return "terrestial"

    classification = property(_get_classification)

    # Auxilliary parameters.

    def _get_rel_axis(self):
       return self.semimajoraxis / self.system.max_planet_semimajoraxis

    rel_axis = property(_get_rel_axis)

    # Image parameters.

    def _get_img_rel_radius(self):
       if self.radius:
           return self.radius / self.system.max_planet_radius * 10
       else:
           return 10

    img_rel_radius = property(_get_img_rel_radius)

    def _get_img_rel_inner_radius(self):
       return self.img_rel_radius - 2 

    img_rel_inner_radius = property(_get_img_rel_inner_radius)

    def _get_img_rel_semimajoraxis(self):
       return self.rel_axis * 250

    img_rel_semimajoraxis = property(_get_img_rel_semimajoraxis)

    def _get_img_line1_y1(self):
        if self.index:
            return 253 + (self.index - 1) * 27

    img_line1_y1 = property(_get_img_line1_y1)

    def _get_img_line2_y1(self):
        return self.img_line1_y1 + 1

    img_line2_y1 = property(_get_img_line2_y1)

    def _get_img_text_y(self):
        return self.img_line1_y1 - 6

    img_text_y = property(_get_img_text_y)

    def _get_img_legend_x2(self):
        return self.img_rel_semimajoraxis + 260

    img_legend_x2 = property(_get_img_legend_x2)

    def _get_img_legend_x1(self):
        return self.img_legend_x2 - 60

    img_legend_x1 = property(_get_img_legend_x1)

    def _get_img_rel_semiminoraxis(self):
       return self.rel_axis * 100

    img_rel_semiminoraxis = property(_get_img_rel_semiminoraxis)

    def _get_img_cx(self):
       return self.img_rel_semimajoraxis + 260

    img_cx = property(_get_img_cx)
