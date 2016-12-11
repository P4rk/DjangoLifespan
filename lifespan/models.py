from __future__ import unicode_literals

from django.db import models

class Country(models.Model):
  country_name = models.CharField(max_length=200)
  country_code = models.CharField(max_length=4)

  def __str__(self):
    return self.country_name

class Rate(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  rate_type = models.CharField(max_length=200)
  rate = models.DecimalField(max_digits=6, decimal_places=3)
  year = models.DateField('data_date')

  def __str__(self):
    return self.rate_type + ':' + str(self.rate) + ':' + str(self.year.year)
