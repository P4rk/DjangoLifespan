from django.test import TestCase
from lifespan import services
from lifespan.models import Country

class ServicesApiIntegrationTestCase(TestCase):

  def test_populate_all_countries(self):
    countries = Country.objects.all() 
    self.assertEquals(len(countries), 0)
    services.populate_all_countries(None)
    countries = Country.objects.all() 
    #The number of countries returned from the api could change
    #from 304
    self.assertEquals(len(countries), 304)

  def test_get_rate_for_country_from_api(self):
    country = services.get_country_from_api('GBR')
    rates = services.get_rate_for_country(country, indicator_name='birth')
    #the number of rates returned from the api could change from
    # 57
    self.assertEquals(len(rates), 57)
    for rate in rates:
      self.assertEquals(rate.rate_type, 'birth')

  def test_get_rate_for_country_with_year_from_api(self):
    country = services.get_country_from_api('GBR')
    rates = services.get_rate_for_country(country, indicator_name='birth', year='2000')
    self.assertEquals(len(rates), 1)
    for rate in rates:
      self.assertEquals(rate.rate_type, 'birth')

