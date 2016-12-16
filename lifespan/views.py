from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from lifespan.models import Country
from lifespan.models import Rate
from lifespan.serializers import CountrySerializer
from lifespan.serializers import RateSerializer
from lifespan.serializers import RateYearSerializer
import requests
from django.db.models import Q
from lifespan import services

# Create your views here.

def home(request):
  """
  Home view, rendering main page.
  """
  context = {}
  return render(request, 'lifespan/index.html', context)

class JSONResponse(HttpResponse):
  """
  Custom responce mapping serailized json objects to a HttpResponse
  """
  def __init__(self, data, **kwargs):
    content = JSONRenderer().render(data)
    kwargs['content_type'] = 'application/json'
    super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def country_list(request):
  """
  A view returning a list of the currently persisted countries as a JSON object
  """
  if request.method == 'GET':
    countries = Country.objects.all().order_by('country_name')
    serializer = CountrySerializer(countries, many=True)
    return JSONResponse(serializer.data)
  return JSONResponse('', status=400)

@csrf_exempt
def country_detail(request, code):
  """
  A view returning a single country loaded from the 3 letter code provided as a JSON object
  """
  if request.method == 'GET':
    country = services.get_country(code)
    serializer = CountrySerializer(country)
    return JSONResponse(serializer.data)
  return JSONResponse('', status=400)

@csrf_exempt
def years_for_country(request, code):
  """
  A view returning a distinct list of years for a country loaded via the 3 letter country code as a JSON object
  """
  if request.method == 'GET':
    country = services.get_country(code)
    services.get_rates_for_country(country)
    rates = Rate.objects.filter(country=country).filter(~Q(rate=0)).values('year').distinct().order_by('-year')
    serializer = RateYearSerializer(rates, many=True)
    return JSONResponse(serializer.data)
  return JSONResponse('', status=400)
    

@csrf_exempt
def rate_for_country(request, code):
  """
  Returns a list of rates for a country loaded via the 3 letter country code.
  Looks for a type and/or year request parameter, if found they are used to limit
  the returned rates as a JSON object
  """
  if request.method == 'GET':
    country = services.get_country(code)
    indicator_name = request.GET.get('type', None) 
    year = request.GET.get('year', None)
    rates = services.get_rates_for_country(country, indicator_name, year)
    serializer = RateSerializer(rates, many=True)
    return JSONResponse(serializer.data)
  return JSONResponse('', status=400)

