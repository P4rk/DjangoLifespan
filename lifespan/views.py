from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from lifespan.models import Country
from lifespan.models import Rate
from lifespan.serializers import CountrySerializer
from lifespan.serializers import RateSerializer
import requests
from lifespan.services import populate_all_countries
from lifespan.services import get_country
from lifespan.services import get_rates_for_country

# Create your views here.

def home(request):
  countries = Country.objects.all()
  context = {'country_list':countries}
  return render(request, 'lifespan/index.html', context)

class JSONResponse(HttpResponse):
  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs['content_type'] = 'application/json'
    super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def country_list(request):
  if request.method == 'GET':
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return JSONResponse(serializer.data)
  return JSONResponse('', status=400)

@csrf_exempt
def country_detail(request, code):
  if request.method == 'GET':
    country = get_country(code)
    serializer = CountrySerializer(country)
    return JSONResponse(serializer.data)
  return JSONResponse('', status=400)

@csrf_exempt
def rate_for_country(request, code):
  if request.method == 'GET':
    country = get_country(code)
    indicator_name = request.GET.get('type', None) 
    year = request.GET.get('year', None)
    rates = get_rates_for_country(country, indicator_name, year)
    serializer = RateSerializer(rates, many=True)
    return JSONResponse(serializer.data)
  return JSONResponse('', status=400)

