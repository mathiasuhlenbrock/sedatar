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

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^astronomical_database/$', 'astronomical_database.views.index'),
    url(r'^astronomical_database/about/$', 'astronomical_database.views.about'),
    url(r'^astronomical_database/List_of_star_catalogues/(?P<catalogue_page_name>[a-zA-Z_0-9\-\+]+)/$', 'astronomical_database.views.catalogue'),
    url(r'^astronomical_database/List_of_star_catalogues/$', 'astronomical_database.views.list_of_catalogues'),
    url(r'^astronomical_database/database/$', 'astronomical_database.views.database'),
    url(r'^astronomical_database/List_of_planetary_systems/(?P<planetary_system_page_name>[a-zA-Z_0-9\-\+\.]+)/$', 'astronomical_database.views.planetary_system'),
    url(r'^astronomical_database/List_of_posts/(?P<post_date>[a-zA-Z_0-9\-\+\,]+)/$', 'astronomical_database.views.post'),
    url(r'^astronomical_database/List_of_posts/$', 'astronomical_database.views.list_of_posts'),
]

admin.site.site_title = 'Database Administration'
admin.site.site_header = 'Database Administration'
