from django.db import models

# Create your models here.

class Crop(models.Model):
    TYPE_CHOICES = [
        ("leaf", "Leaf"),
        ("root", "Root"),
        ("tuber", "Tuber"),
        ("stalk", "Stalk"),
        ("fruit", "Fruit"),
        ("mushroom", "Mushroom"),
        ("seed", "Seed"),
        ("cereal", "Cereal"),
        ("legume", "Legume"),
        ("nut", "Nut"),
        ("spice", "Spice"),
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(choices=TYPE_CHOICES)
    sowing_range = models.DateField()
    harvestring_range = models.DateField()
    LIFE_CYCLE_CHOICES = (
        ("perennial", "Perennial"),
        ("biennial", "Biennial"),
        ("many_years", "Many Years"),
    )
    life_cycle = models.CharField(max_length=20, choices=LIFE_CYCLE_CHOICES)

  
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
