#from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts      import get_object_or_404, render_to_response

from astronomical_database.models import * 

# Create your views here.

def about(request):
    return render_to_response('astronomical_database/about.html')

def catalogue(request, catalogue_page_name):
    catalogue = get_object_or_404(Catalogue, name = catalogue_page_name.replace("_", " "))
    paginator = Paginator(catalogue.planetarysystem_set.order_by('name'), 80)

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

    return render_to_response('astronomical_database/catalogue.html', {'catalogue': catalogue, 'list_of_planetary_systems' : list_of_planetary_systems})

def list_of_catalogues(request):
    paginator = Paginator(Catalogue.objects.order_by('name'), 40)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        list_of_catalogues = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list_of_catalogues = paginator.page(paginator.num_pages)

    return render_to_response('astronomical_database/list_of_catalogues.html', {'list_of_catalogues': list_of_catalogues})

def database(request):
    paginator = Paginator(Category.objects.order_by('name'), 40)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        list_of_categories = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list_of_categories = paginator.page(paginator.num_pages)

    return render_to_response('astronomical_database/database.html', {'list_of_categories': list_of_categories})

def index(request):
    return render_to_response('astronomical_database/index.html')

def planetary_system(request, planetary_system_page_name):
    planetary_system = get_object_or_404(PlanetarySystem, name = planetary_system_page_name.replace("_", " "))
    paginator = Paginator(planetary_system.planet_set.order_by('semimajoraxis'), 20)

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

    return render_to_response('astronomical_database/planetary_system.html', {'planetary_system': planetary_system, 'list_of_planets' : list_of_planets})

def post(request, post_date):
    post = get_object_or_404(Post, date = post_date)

    return render_to_response('astronomical_database/post.html', {'post': post})

def list_of_posts(request):
    paginator = Paginator(Post.objects.order_by('-date'), 20)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        list_of_posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list_of_posts = paginator.page(paginator.num_pages)

    return render_to_response('astronomical_database/list_of_posts.html', {'list_of_posts': list_of_posts})
