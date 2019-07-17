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
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^About/$', views.about, name='about'),
    url(r'^Admin/', admin.site.urls),
    url(r'^Answer/$', views.answer, name='answer'),
    url(r'^Astronomical_database/', include('astronomical_database.urls')),
    url(r'^List_of_databases/$', views.list_of_databases, name='list_of_databases'),
    url(r'^List_of_posts/(?P<post_date>[a-zA-Z_0-9\-]+)/$', views.post, name='post'),
    url(r'^List_of_posts/$', views.list_of_posts, name='list_of_posts'),
]

admin.site.site_title = 'Database Administration'
admin.site.site_header = 'Database Administration'
