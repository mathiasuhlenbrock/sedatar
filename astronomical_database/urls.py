from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^List_of_categories/$',
        views.list_of_categories,
        name='list_of_categories'
    ),
    url(
        r'^List_of_star_catalogues/(?P<catalogue_page_name>[a-zA-Z_0-9\-+.]+)/$',
        views.catalogue,
        name='catalogue'
    ),
    url(
        r'^List_of_star_catalogues/$',
        views.list_of_catalogues,
        name='list_of_catalogues'
    ),
    url(
        r'^List_of_planetary_systems/(?P<planetary_system_page_name>[a-zA-Z_0-9\-+.]+)/$',
        views.planetary_system,
        name='planetary_system'
    ),
    url(
        r'^List_of_planets/(?P<planet_page_name>[a-zA-Z_0-9\-+.]+)/$',
        views.planet,
        name='planet'
    ),
]
