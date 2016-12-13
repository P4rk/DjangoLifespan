from rest_framework import serializers
from lifespan.models import Country
from lifespan.models import Rate

class CountrySerializer(serializers.ModelSerializer):
  class Meta:
    model = Country
    field = ('country_name','country_code')

class RateSerializer(serializers.ModelSerializer):
  country = serializers.ReadOnlyField(source='country.country_code')
  class Meta:
    model = Rate
    fields = ('country', 'rate_type', 'rate', 'year')

class RateYearSerializer(serializers.ModelSerializer):
  country = serializers.ReadOnlyField(source='country.country_code')
  date = serializers.DateField(source='year', format='%Y')
  class Meta:
    model = Rate
    fields = ('country','date')
