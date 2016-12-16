from __future__ import unicode_literals

from django.db import models

class Country(models.Model):
  """
  A country object containing the country name and 3 letter country code
  """
  country_name = models.CharField(max_length=200)
  country_code = models.CharField(max_length=4)

  def __str__(self):
    return self.country_name

class Rate(models.Model):
  """
  A rate object containing information about an indicator for a country
  This object contains the rate type e.g. 'birth' or 'lifexpectancy',
  the rate as a decimal of 6 digits, with 3 decimal places and, a year
  that this rate belongs to.
  """
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  rate_type = models.CharField(max_length=200)
  rate = models.DecimalField(max_digits=6, decimal_places=3)
  year = models.DateField('data_date')

  def __str__(self):
    return self.rate_type + ':' + str(self.rate) + ':' + str(self.year.year)
