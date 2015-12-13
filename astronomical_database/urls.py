from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^about/$', views.about, name = 'about'),
    url(r'^List_of_star_catalogues/(?P<catalogue_page_name>[a-zA-Z_0-9\-\+]+)/$', views.catalogue, name = 'catalogue'),
    url(r'^List_of_star_catalogues/$', views.list_of_catalogues, name = 'list_of_catalogues'),
    url(r'^database/$', views.database, name = 'database'),
    url(r'^List_of_planetary_systems/(?P<planetary_system_page_name>[a-zA-Z_0-9\-\+\.]+)/$', views.planetary_system, name = 'planetary_system'),
    url(r'^List_of_posts/(?P<post_date>[a-zA-Z_0-9\-\+\,]+)/$', views.post, name = 'post'),
    url(r'^List_of_posts/$', views.list_of_posts, name = 'list_of_posts'),
]
