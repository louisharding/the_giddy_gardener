from django.db import models
from django.contrib.auth.models import User

# Crop type 
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
    ("herb", "Herb"),
    ("flower", "Flower"),
]

# Subtype of crop
SUBTYPE_MAP = {
    "fruit": (
        ("drupe", "Drupe"),
        ("berry", "Berry"),
        ("citrus", "Citrus"),
        ("pome", "Pome"),
    ),
    "leaf": (
        ("brassica", "Brassica"),
        ("salad", "Salad Leaf"),
    ),
    "root": (
        ("taproot", "Taproot"),
        ("fibrous", "Fibrous"),
    ),
}
SUBTYPE_CHOICES = []
for sublist in SUBTYPE_MAP.values():
    SUBTYPE_CHOICES.extend(sublist)
seen = set()
uniq_subtypes = []
for code, label in SUBTYPE_CHOICES:
    if code not in seen:
        uniq_subtypes.append((code, label))
        seen.add(code)
SUBTYPE_CHOICES = tuple(uniq_subtypes)


LIFE_CYCLE_CHOICES = (
    ("perennial", "Perennial"),
    ("biennial", "Biennial"),
    ("annual", "Annual"),
)

class Crop(models.Model):
    common_name = models.CharField(max_length=200, null=False, blank=False)                      # Braeburn Apple
    scientific_name = models.CharField(max_length=200, unique=True, null=False, blank=False)     # PK Breaburnicus Appeleo
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=False, blank=False)        # Fruit
    #name = models.CharField(max_length=200, unique=True)

    life_cycle = models.CharField(max_length=50, choices=LIFE_CYCLE_CHOICES)
    # Sowing and Harvesting ranges
    sowing_date_earliest = models.DateField()
    sowing_date_latest = models.DateField()

    harvesting_date_earliest = models.DateField()
    harvesting_date_latest = models.DateField()

    def __str__(self):
        # Return a human-friendly representation for admin and debugging
        if getattr(self, 'common_name', None) and getattr(self, 'scientific_name', None):
            return f"{self.common_name} ({self.scientific_name})"
        # Fallback to the default object representation if fields are missing
        return super().__str__()






# A garden is simply where a user stores their saved allotments
class Garden(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gardener")
    
    def __str__(self):
        return f"{self.owner}'s Garden"

    # Nice to haves:
    """
    # country = ""
    # postcode = ""
    # city = ""
    # climate = "" choice
    # localPests = ""
    # seaLevel = ""
    """   



# Allotments contain a single crop and are used to describe the situation where said crop will be grown :) ::leaf emoji
# Deleted upon 
class Allotment(models.Model):
    name = models.CharField(max_length=200, default="Allotment")    #Eg flourpatch 1, runnerbean square, potato pathway
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name="garden")
    current_crop = models.ForeignKey(Crop, null=True, blank=True, on_delete=models.SET_NULL, related_name="allotments")
    # Nice to haves:
    """
    # area = "" # in meters square none of that boomer nonsense
    # coverage = "" #dropdown list eg eg- indoor, outdoor, greenhouse, coldframe etc
    # soilTypes = "" #inclusive dropdown list
    # soilAcidity = "" #float, allowed range : 5 to 9
    
    # perhaps an option to make an allotment public, allowing other users to import an allotment into their garden
    # must consider data sanitation though! 
    """

