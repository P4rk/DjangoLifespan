from django.test import TestCase
from lifespan.models import Country
from lifespan.models import Rate
from lifespan.serializers import CountrySerializer
from lifespan.serializers import RateSerializer
from lifespan.serializers import RateYearSerializer

class SerializersTestCase(TestCase):

  def setUp(self):
    country = Country.objects.create(country_name='test_name', country_code='code')
    Rate.objects.create(country=country, rate_type='test_rate', rate=0.5, year='2000-01-01')

  def testCountrySerializer(self):
    country = Country.objects.get(country_code='code')
    serializer = CountrySerializer(country)
    self.assertEquals(str(serializer.data), "{'country_name': u'test_name', 'country_code': u'code'}")

  def testRateSerializer(self):
    rate = Rate.objects.get(rate_type='test_rate')
    serializer = RateSerializer(rate)
    self.assertEquals(str(serializer.data), "{'country': u'code', 'rate': u'0.500', 'rate_type': u'test_rate', 'year': '2000-01-01'}")
    serializer = RateYearSerializer(rate)
    self.assertEquals(str(serializer.data), "{'date': '2000', 'country': u'code'}")
