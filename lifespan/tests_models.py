from django.test import TestCase
from lifespan.models import Country
from lifespan.models import Rate

class CountryTestCase(TestCase):
  def setUp(self):
    country_one = Country.objects.create(country_name="testCountryOne", country_code="TCO")
    country_two = Country.objects.create(country_name="testCountryTwo", country_code="TCT")

    Rate.objects.create(country=country_one, rate_type = "Rate1", rate = 0.5, year='2000-01-01')
    Rate.objects.create(country=country_one, rate_type = "Rate2", rate = 100, year='2000-01-01')

  def test_country_too_string(self):
    country_one = Country.objects.get(country_code="TCO")
    self.assertEquals(str(country_one), 'testCountryOne')

    country_two = Country.objects.get(country_code="TCT")
    self.assertEquals(str(country_two), 'testCountryTwo')

  def test_rate_too_string (self):
    rate_one = Rate.objects.get(rate_type = 'Rate1')
    self.assertEquals(str(rate_one), 'Rate1:0.500:2000')

    rate_two = Rate.objects.get(rate_type = 'Rate2')
    self.assertEquals(str(rate_two), 'Rate2:100.000:2000')
