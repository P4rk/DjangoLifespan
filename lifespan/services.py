from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from lifespan.models import Country
from lifespan.models import Rate
import datetime
import requests 

#World bank api indicator to rate type dictionary
RATES = {'birth':'SP.DYN.CBRT.IN','lifespan':'SP.DYN.LE00.IN' }

@csrf_exempt
def populate_all_countries(request):
  """
  Populates the database with a list of countries form the world bank api
  """
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
  return HttpResponse(status=201)

def get_country(code):
  """
  Retrieves country for the country code from the database.
  If there is no entry in the database it's attempted to be retrieved from the world bank api
  If there is no entry in the api a None is returned
  """
  try:
    return Country.objects.get(country_code=code)
  except Country.DoesNotExist:
    return get_country_from_api(code)

def get_country_from_api(code):
  """
  Retrieves country for the country code from the world bank api.
  If there is no entry in the api a None is returned
  """
  url = 'http://api.worldbank.org/countries/' + code
  params = {'format': 'json'}
  r = requests.get(url, params=params)
  jsonCountry = r.json()
  try: 
    name = jsonCountry[1][0].get('name')
    code = jsonCountry[1][0].get('id')
    return Country.objects.create(country_name=name, country_code=code) 
  #except IndexError, the world bank api returns 200's even if there isn't a country for that country code
  except IndexError:
    return None

def get_rates_for_country(country, indicator_name=None, year=None):
  """
  Returns a list of rates for the country
  Will return all indicators for all year if none are supplied
  """
  if indicator_name:
    return get_rate_for_country(country, indicator_name, year=year)
  else:
    rates = []
    indicator_name = RATES.keys()
    for indicator in indicator_name:
        rates.extend(get_rate_for_country(country, indicator, year=year))
    return rates


def get_rate_for_country(country, indicator_name, year=None):
  """
  Returns a list of rates of a country for a indicator.
  Will return all years for this indicator if no year is supplied
  """
  try:
    if year:
      return [Rate.objects.get(country=country, rate_type=indicator_name, year=conver_year_to_date(year))]
    else:
      rates = Rate.objects.filter(country=country, rate_type=indicator_name)
      if len(rates) == 0:
        return get_and_persist_rate(country, indicator_name)
      return rates
  except Rate.DoesNotExist:
    get_and_persist_rate(country, indicator_name)
    return [Rate.objects.get(country=country, rate_type=indicator_name, year=conver_year_to_date(year))]

def get_and_persist_rate(country, indicator_name):
  """
  Retrives a rate, using the indicator name for the specified country.
  The rates for all years are retrived from the world bank api, persisted to the datebase nad returned.
  """
  created_rates = []
  url = 'http://api.worldbank.org/countries/' + country.country_code + '/indicators/' + RATES[indicator_name]
  params = {'format': 'json'}
  r = requests.get(url, params=params)
  rates = r.json()
  page_number = rates[0].get('pages')
  for page in range(0 , page_number if page_number else 0):
    params = {'format': 'json', 'page':page+1}
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
  """
  Converts a YYYY string to a datetime object on the 1st January YYYY
  """
  return datetime.date(int(year),01,01)
