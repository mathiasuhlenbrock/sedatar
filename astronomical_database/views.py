import re
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import get_object_or_404, render
from astronomical_database.models import *


def convert_to_nth_numeric_component(s, n):
    """
    Converts a string containing one or multiple numeric components to the nth component.
    Example: For n = 1, 'K2-31' is converted to 31.
    Sorts exceptions to the front.
    """
    try:
        numeric_components = re.findall(r'\d+', s)
        return int(numeric_components[n])
    except IndexError:
        return 0
    except TypeError:
        return 0


def sort_by(iterable, strategy):
    """
    Strategies:
      0: alphabetical sorting
      n (not 0): sorting according to the nth numerical string component
    """
    if strategy == 0:
        ordered_iterable = sorted(
            iterable, key=lambda item: item.name
        )
    else:
        ordered_iterable = sorted(
            iterable, key=lambda item: convert_to_nth_numeric_component(item.name, strategy - 1)
        )
    return ordered_iterable


def catalogue(request, catalogue_page_name):
    the_catalogue = get_object_or_404(Catalogue, name=catalogue_page_name.replace('_', ' '))
    # Alternatively consider using custom Manager.
    ordered_catalogue = sort_by(the_catalogue.planetarysystem_set.all(), the_catalogue.ordering_strategy)
    paginator = Paginator(ordered_catalogue, 80)
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
    return render(
        request,
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
    return render(
        request,
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
    return render(
        request,
        'astronomical_database/list_of_categories.html',
        {'list_of_categories': the_list_of_categories}
    )


def planet(request, planet_page_name):
    the_planet = get_object_or_404(Planet, name=planet_page_name.replace('_', ' '))
    return render(request, 'astronomical_database/planet.html', {'planet': the_planet})


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
    return render(
        request,
        'astronomical_database/planetary_system.html',
        {'planetary_system': the_planetary_system, 'list_of_planets': list_of_planets}
    )
