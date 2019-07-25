from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context_processors import csrf
from sedatar.forms import *
from sedatar.models import *


def about(request):
    return render_to_response('sedatar/about.html')


def answer(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        search = Search(question=form.cleaned_data['question'])
        search.save()
        return render_to_response('sedatar/answer.html', {'search': search})


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/sedatar/answer/', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()
    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('sedatar/index.html', c)


def list_of_databases(request):
    paginator = Paginator(Database.objects.order_by('name'), 40)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        the_list_of_databases = paginator.page(page)
    except (EmptyPage, InvalidPage):
        the_list_of_databases = paginator.page(paginator.num_pages)
    return render_to_response('sedatar/list_of_databases.html', {'list_of_databases': the_list_of_databases})


def list_of_posts(request):
    paginator = Paginator(Post.objects.order_by('-date'), 20)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        the_list_of_posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        the_list_of_posts = paginator.page(paginator.num_pages)
    return render_to_response('sedatar/list_of_posts.html', {'list_of_posts': the_list_of_posts})


def post(request, post_date):
    the_post = get_object_or_404(Post, date=post_date)
    return render_to_response('sedatar/post.html', {'post': the_post})
