from django.conf.urls import url

from lifespan import views
from lifespan import services

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'country/$', views.country_list, name='country_list'),
    url(r'country/populate', services.populate_countries, name='populate_country'),
    url(r'country/(?P<code>\w+)/$', views.country_detail, name='country_detail'),
    url(r'country/(?P<code>\w+)/rate/$', views.rate_for_country, name='rates_for_country'),
    url(r'country/(?P<code>\w+)/rate/(?P<indicator_name>\w+)/$', views.rate_for_country, name='rates_for_country_with_inicator'),
    url(r'country/(?P<code>\w+)/rate/(?P<indicator_name>\w+)/year/(?P<year>\d{4})/$', views.rate_for_country, name='rates_for_country_with_inicator_with_year'),
]
