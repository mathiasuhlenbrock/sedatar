from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import get_object_or_404, render_to_response
from astronomical_database.models import *


def catalogue(request, catalogue_page_name):
    the_catalogue = get_object_or_404(Catalogue, name=catalogue_page_name.replace('_', ' '))
    paginator = Paginator(the_catalogue.planetarysystem_set.order_by('name'), 80)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        list_of_planetary_systems = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list_of_planetary_systems = paginator.page(paginator.num_pages)
    return render_to_response(
        'astronomical_database/catalogue.html',
        {'catalogue': the_catalogue, 'list_of_planetary_systems': list_of_planetary_systems}
    )


def list_of_catalogues(request):
    paginator = Paginator(Catalogue.objects.order_by('name'), 40)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        the_list_of_catalogues = paginator.page(page)
    except (EmptyPage, InvalidPage):
        the_list_of_catalogues = paginator.page(paginator.num_pages)
    return render_to_response(
        'astronomical_database/list_of_catalogues.html',
        {'list_of_catalogues': the_list_of_catalogues}
    )


def list_of_categories(request):
    paginator = Paginator(Category.objects.order_by('name'), 40)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        the_list_of_categories = paginator.page(page)
    except (EmptyPage, InvalidPage):
        the_list_of_categories = paginator.page(paginator.num_pages)
    return render_to_response(
        'astronomical_database/list_of_categories.html',
        {'list_of_categories': the_list_of_categories}
    )


def planet(request, planet_page_name):
    the_planet = get_object_or_404(Planet, name=planet_page_name.replace('_', ' '))
    return render_to_response('astronomical_database/planet.html', {'planet': the_planet})


def planetary_system(request, planetary_system_page_name):
    the_planetary_system = get_object_or_404(PlanetarySystem, name=planetary_system_page_name.replace('_', ' '))
    paginator = Paginator(the_planetary_system.planet_set.order_by('semimajoraxis'), 20)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        list_of_planets = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list_of_planets = paginator.page(paginator.num_pages)
    return render_to_response(
        'astronomical_database/planetary_system.html',
        {'planetary_system': the_planetary_system, 'list_of_planets': list_of_planets}
    )
