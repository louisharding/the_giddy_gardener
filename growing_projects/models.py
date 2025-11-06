from django.db import models

# Create your models here.

class Crop(models.Model):
    #ID primary key
    name = ""
    type = ""
    sowing_range = ""
    harvestring_range = ""
    life_cycle = ""

  
class Allotment(models.Model):
    id = ""
    name = ""
    area = "" # in meters square
    soilTypes = "" #inclusive dropdown list
    climate = "" #dropdownlist
    coverage = "" #dropdown list eg eg- indoor, outdoor, greenhouse, coldframe etc
    seaLevel = ""
    country = ""
    city = ""
    localPests = ""
    soilAcidity = ""
    postcode = ""
