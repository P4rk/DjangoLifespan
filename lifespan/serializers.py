from rest_framework import serializers
from lifespan.models import Country
from lifespan.models import Rate

class CountrySerializer(serializers.ModelSerializer):
  class Meta:
    model = Country
    field = ('country_name','country_code')

class RateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rate
    fields = ('country', 'rate_type', 'rate', 'year')
