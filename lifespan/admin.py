from django.contrib import admin

# Register your models here.
from lifespan.models import Country
from lifespan.models import Rate

admin.site.register(Country)
admin.site.register(Rate)
