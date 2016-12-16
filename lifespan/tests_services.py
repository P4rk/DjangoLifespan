from django.test import TestCase
from lifespan import services
from lifespan.models import Country
from lifespan.models import Rate 


class ServicesTestCase(TestCase):

  BIRTH_INDICATOR_NAME = 'birth'
  LIFESPAN_INDICATOR_NAME = 'lifespan'

  def setUp(self):
    country = Country.objects.create(country_name='test_country', country_code='test')
    Rate.objects.create(country=country, rate_type=ServicesTestCase.BIRTH_INDICATOR_NAME, rate='0.5', year='2000-01-01')
    Rate.objects.create(country=country, rate_type=ServicesTestCase.BIRTH_INDICATOR_NAME, rate='0.5', year='2001-01-01')
    Rate.objects.create(country=country, rate_type=ServicesTestCase.LIFESPAN_INDICATOR_NAME, rate='0.5', year='2000-01-01')
    Rate.objects.create(country=country, rate_type=ServicesTestCase.LIFESPAN_INDICATOR_NAME, rate='0.5', year='2001-01-01')

  def test_get_country(self):
    country = services.get_country('GBR')
    self.assertEquals(country.country_name, 'United Kingdom')

  def test_get_country_from_api(self):
    country = services.get_country_from_api('GBR')
    self.assertEquals(country.country_name, 'United Kingdom')

    none_country = services.get_country_from_api('UNKNOWN')
    self.assertEquals(none_country, None)

  def test_get_rates_for_country(self):
    country = Country.objects.get(country_code='test')

    all_rates = services.get_rates_for_country(country)
    self.assertEquals(len(all_rates), 4)

    birth_rates = services.get_rates_for_country(country, indicator_name=ServicesTestCase.BIRTH_INDICATOR_NAME)
    self.assertEquals(len(birth_rates), 2)
    for rate in birth_rates:
      self.assertEquals(rate.rate_type,ServicesTestCase.BIRTH_INDICATOR_NAME)

    lifespan_rates = services.get_rates_for_country(country, indicator_name=ServicesTestCase.LIFESPAN_INDICATOR_NAME)
    self.assertEquals(len(lifespan_rates), 2)
    for rate in lifespan_rates:
      self.assertEquals(rate.rate_type,ServicesTestCase.LIFESPAN_INDICATOR_NAME)

    rates_2000 = services.get_rates_for_country(country, year='2000')
    self.assertEquals(len(rates_2000), 2)
    for rate in rates_2000:
      self.assertEquals(str(rate.year.year), '2000')

    rates_2001 = services.get_rates_for_country(country, year='2001')
    self.assertEquals(len(rates_2001), 2)
    for rate in rates_2001:
      self.assertEquals(str(rate.year.year), '2001')

  def test_convert_year_to_date(self):
    date = services.conver_year_to_date('2000')
    self.assertEquals(str(date.year), '2000')
    self.assertEquals(str(date.month), '1')
    self.assertEquals(str(date.day), '1')


