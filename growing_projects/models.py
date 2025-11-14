from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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

class Crop(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(choices=TYPE_CHOICES)
    """
    sowing_range = models.DateField()
    harvestring_range = models.DateField()
    LIFE_CYCLE_CHOICES = (
        ("perennial", "Perennial"),
        ("biennial", "Biennial"),
        ("many_years", "Many Years"),
    )
    life_cycle = models.CharField(max_length=20, choices=LIFE_CYCLE_CHOICES)
    add method for returning sowing ranges and harvesting ranges
    add method for returning season range 
    """

  
class Allotment(models.Model):
    name = models.CharField(max_length=200, default="Allotment")
    garden = models.CharField(max_length=200, default="garden")
    """
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
    perhaps an option to make an allotment public, doing so allows users to create premade common allotments for other users to 
    select from and change as they see fit
    there would need to be a limit as to how many public allotments could be made by a user
    as to avoid griefing and spamming
    """

# Each user can add a garden, a garden can contain multiple allotments,
# A garden is simply where a user stores their saved allotments
class Garden(models.Model):
    name = models.CharField(max_length=200, default="My Garden")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gardener")

    
