"""
Documentation goes here.
"""

from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.context_processors import csrf

from sedatar.forms import SearchForm
from sedatar.models import Database, Post, Search, SearchWikidata


def about(request):
    """
    Documentation goes here.
    """
    return render(request, 'sedatar/about.html')


def answer(request):
    """
    Documentation goes here.
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = Search(question=form.cleaned_data['question'])
            search_wikidata = SearchWikidata(question=form.cleaned_data['question'])
        else:
            return
    else:
        search = Search(question=request.GET.get('question'))
        search_wikidata = SearchWikidata(question=request.GET.get('question'))
    paginator = Paginator(search.answers, 1)
    paginator_wikidata = Paginator(search_wikidata.answers, 1)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
        page_wikidata = int(request.GET.get('page_wikidata', '1'))
    except ValueError:
        page = 1
        page_wikidata = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        the_list_of_answers = paginator.page(page)
        the_list_of_wikidata_answers = paginator_wikidata.page(page_wikidata)
    except (EmptyPage, InvalidPage):
        the_list_of_answers = paginator.page(paginator.num_pages)
        the_list_of_wikidata_answers = paginator_wikidata.page(paginator_wikidata.num_pages)
    return render(
        request,
        'sedatar/answer.html',
        {
            'question': search.question,
            'list_of_answers': the_list_of_answers,
            'list_of_wikidata_answers': the_list_of_wikidata_answers
        }
    )


def index(request):
    """
    Documentation goes here.
    """
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
    return render(request, 'sedatar/index.html', c)


def list_of_databases(request):
    """
    Documentation goes here.
    """
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
    return render(request, 'sedatar/list_of_databases.html', {'list_of_databases': the_list_of_databases})


def list_of_dependencies(request):
    """
    Documentation goes here.
    """
    return render(request, 'sedatar/list_of_dependencies.html')


def list_of_posts(request):
    """
    Documentation goes here.
    """
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
    return render(request, 'sedatar/list_of_posts.html', {'list_of_posts': the_list_of_posts})


def post(request, post_date):
    """
    Documentation goes here.
    """
    the_post = get_object_or_404(Post, date=post_date)
    return render(request, 'sedatar/post.html', {'post': the_post})
