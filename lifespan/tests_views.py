from django.test import TestCase
from lifespan import views
from lifespan.models import Country
from lifespan.models import Rate
from django.http import HttpRequest
import json

class ViewTestCase(TestCase):
  bad_request = HttpRequest() 
  good_request = HttpRequest()

  BIRTH_INDICATOR_NAME = 'birth'
  LIFESPAN_INDICATOR_NAME = 'lifespan'

  def setUp(self):
    ViewTestCase.bad_request.method = 'POST'
    ViewTestCase.good_request.method = 'GET'

    countryOne = Country.objects.create(country_name="testCountryOne", country_code="TCO")
    countryTwo = Country.objects.create(country_name="testCountryTwo", country_code="TCT")

    Rate.objects.create(country=countryOne, rate_type = ViewTestCase.BIRTH_INDICATOR_NAME, rate = 0.5, year='2000-01-01')
    Rate.objects.create(country=countryOne, rate_type = ViewTestCase.BIRTH_INDICATOR_NAME, rate = 0.5, year='2001-01-01')
    Rate.objects.create(country=countryOne, rate_type = ViewTestCase.LIFESPAN_INDICATOR_NAME, rate = 100, year='2000-01-01')
    Rate.objects.create(country=countryOne, rate_type = ViewTestCase.LIFESPAN_INDICATOR_NAME, rate = 100, year='2001-01-01')

  def test_home(self):
    rsp = views.home(ViewTestCase.good_request)
    self.assertEquals(rsp.status_code, 200)

  def test_country_list(self):
    rsp = views.country_list(ViewTestCase.bad_request)
    self.assertEquals(rsp.status_code, 400)

    rsp = views.country_list(ViewTestCase.good_request)
    self.assertEquals(rsp.status_code, 200)

    content = json.loads(rsp.content)
    self.assertEquals(len(content), 2)
    for obj in content:
      self.assertIn(obj.get('country_name'), ['testCountryOne', 'testCountryTwo'])
      self.assertIn(obj.get('country_code'), ['TCO', 'TCT'])

  def test_country_detail(self):
    rsp = views.country_detail(ViewTestCase.bad_request, 'TCO')
    self.assertEquals(rsp.status_code, 400)

    rsp = views.country_detail(ViewTestCase.good_request, 'TCO')
    self.assertEquals(rsp.status_code, 200)

    content = json.loads(rsp.content)
    self.assertEquals(content.get('country_name'), 'testCountryOne')
    self.assertEquals(content.get('country_code'), 'TCO')
    
  def test_years_for_country (self):
    rsp = views.years_for_country(ViewTestCase.bad_request, 'TCO')
    self.assertEquals(rsp.status_code, 400)

    rsp = views.years_for_country(ViewTestCase.good_request, 'TCO')
    self.assertEquals(rsp.status_code, 200)
    content = json.loads(rsp.content)
    for date in content:
      self.assertIn(date.get('date'), ['2000', '2001'])

  def test_rate_for_country(self):
    rsp = views.rate_for_country(ViewTestCase.bad_request, 'TCO')
    self.assertEquals(rsp.status_code, 400)

    rsp = views.rate_for_country(ViewTestCase.good_request, 'TCO')
    self.assertEquals(rsp.status_code, 200)

    content = json.loads(rsp.content)
    for rate in content: 
      self.assertEquals(rate.get('country'), 'TCO')
      self.assertIn(rate.get('year'), ['2000-01-01', '2001-01-01'])
      self.assertIn(rate.get('rate_type'), [ViewTestCase.BIRTH_INDICATOR_NAME, ViewTestCase.LIFESPAN_INDICATOR_NAME])

    ViewTestCase.good_request.GET['type'] = 'birth'
    ViewTestCase.good_request.GET['year'] = '2000'
    rsp = views.rate_for_country(ViewTestCase.good_request, 'TCO')
    self.assertEquals(rsp.status_code, 200)

    content = json.loads(rsp.content)
    for rate in content: 
      self.assertEquals(rate.get('country'), 'TCO')
      self.assertIn(rate.get('year'), ['2000-01-01'])
      self.assertIn(rate.get('rate_type'), [ViewTestCase.BIRTH_INDICATOR_NAME ])
