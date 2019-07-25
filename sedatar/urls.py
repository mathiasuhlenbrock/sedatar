"""sedatar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import include, path, re_path
from django.contrib import admin
from . import views

urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'About/',
        views.about,
        name='about'
    ),
    path(
        'Admin/',
        admin.site.urls
    ),
    path(
        'Answer/',
        views.answer,
        name='answer'
    ),
    path(
        'Astronomical_database/',
        include('astronomical_database.urls')
    ),
    path(
        'List_of_databases/',
        views.list_of_databases,
        name='list_of_databases'
    ),
    re_path(
        r'^List_of_posts/(?P<post_date>[a-zA-Z_0-9-+.]+)/$',
        views.post,
        name='post'
    ),
    path(
        'List_of_posts/',
        views.list_of_posts,
        name='list_of_posts'
    ),
]

admin.site.site_title = 'Database Administration'
admin.site.site_header = 'Database Administration'
