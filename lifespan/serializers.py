from rest_framework import serializers
from lifespan.models import Country
from lifespan.models import Rate

class CountrySerializer(serializers.ModelSerializer):
  """
  Default serializer for the Country model
  """
  class Meta:
    model = Country
    fields = ('country_name','country_code')

class RateSerializer(serializers.ModelSerializer):
  """
  Default serializer for the Rate model
  """
  country = serializers.ReadOnlyField(source='country.country_code')
  class Meta:
    model = Rate
    fields = ('country', 'rate_type', 'rate', 'year')

class RateYearSerializer(serializers.ModelSerializer):
  """
  Rate Serializer returning the year and country for this rate.
  """
  country = serializers.ReadOnlyField(source='country.country_code')
  date = serializers.DateField(source='year', format='%Y')
  class Meta:
    model = Rate
    fields = ('country','date')
