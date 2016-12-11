from django.http import HttpResponse
from lifespan.models import Country
from lifespan.models import Rate
import datetime
import requests 

RATES = {'birth':'SP.DYN.CBRT.IN','lifespan':'SP.DYN.LE00.IN' }

def populate_countries(request):
    populate_all_countries()
    return HttpResponse(status=201)

def populate_all_countries():
  url = 'http://api.worldbank.org/countries' 
  params = {'format': 'json'}
  r = requests.get(url, params=params)
  countries = r.json()
  for page in range(1 ,countries[0].get('pages')+1):
    params['page'] = page
    r = requests.get(url, params=params)
    countries = r.json()
    for country in range(0, len(countries[1])):
        name = countries[1][country].get('name')
        code = countries[1][country].get('id')
        Country.objects.get_or_create(country_name=name, country_code=code) 

def get_country(code):
  try:
    return Country.objects.get(country_code=code)
  except Country.DoesNotExist:
    url = 'http://api.worldbank.org/countries/' + code
    params = {'format': 'json'}
    r = requests.get(url, params=params)
    jsonCountry = r.json()
    name = jsonCountry[1][0].get('name')
    code = jsonCountry[1][0].get('id')
    return Country.objects.create(country_name=name, country_code=code) 

def get_rates_for_country(country, indicator_name=None, year=None):
  if indicator_name:
    return get_rate_for_country(country, indicator_name, year=year)
  else:
    rates = []
    indicator_name = RATES.keys()
    for indicator in indicator_name:
        rates.extend(get_rate_for_country(country, indicator, year=year))
    return rates


def get_rate_for_country(country, indicator_name, year=None):
  try:
    if year:
      return [Rate.objects.get(country=country, rate_type=indicator_name, year=conver_year_to_date(year))]
    else:
      rates = Rate.objects.filter(country=country, rate_type=indicator_name)
      if len(rates) == 0:
        return get_and_persist_rate(country, indicator_name, year=year)
      return rates
  except Rate.DoesNotExist:
    return get_and_persist_rate(country, indicator_name, year=year)

def get_and_persist_rate(country, indicator_name, year=None):
  created_rates = []
  url = 'http://api.worldbank.org/countries/' + country.country_code + '/indicators/' + RATES[indicator_name]
  params = {'format': 'json'}
  if year:
    params['year'] = date + ':' + date
  r = requests.get(url, params=params)
  rates = r.json()
  for page in range(0 , rates[0].get('pages')):
    params = {'format': 'json', 'page':page+1}
    if year:
      params['year'] = year + ':' + year
    r = requests.get(url, params=params)
    rates = r.json()
    for rate in range(0, len(rates[1])):
      value = rates[1][rate].get('value')
      date = rates[1][rate].get('date')
      if value == None:
        value = 0
      rate = Rate.objects.create(country=country, rate_type=indicator_name, rate=value, year=conver_year_to_date(date))
      created_rates.append(rate)
  return created_rates


def conver_year_to_date(year):
  return datetime.date(int(year),01,01)
