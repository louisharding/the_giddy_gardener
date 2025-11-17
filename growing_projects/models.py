from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

# A crop is grown in an allotment. Crops have multiple properties and can only be effected by admins
class Crop(models.Model):
    scientific_name = models.CharField(max_length=200, unique=True, null=True, blank=True)                      # PK Breaburnicus Appeleo
    common_name = models.CharField(max_length=200, null=True, blank=True, default="Please add common name")     # Braeburn Apple
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=False, blank=False)                       # Fruit
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    # Life cycle; how the crop grows, matures and yields throughout it's life
    life_cycle = models.CharField(max_length=50, choices=LIFE_CYCLE_CHOICES, null=True, blank=True)
    # Sowing & Harvesting ranges; the earliest and latest a crop can be sown and harvested
    sowing_date_earliest = models.DateField(null=True, blank=True)
    sowing_date_latest = models.DateField(null=True, blank=True)
    harvesting_date_earliest = models.DateField(null=True, blank=True)
    harvesting_date_latest = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('growing_projects:crop_detail', kwargs={'slug': self.slug})
    def __str__(self):
        # Return a human-friendly representation for admin and debugging
        if getattr(self, 'common_name', None) and getattr(self, 'scientific_name', None):
            return f"{self.common_name} ({self.scientific_name})"
        # Fallback to the default object representation if fields are missing
        return super().__str__()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('growing_projects:crop_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Auto-generate slug from common_name if not provided
        from django.utils.text import slugify

        if not self.slug:
            base = slugify(self.common_name or self.scientific_name)[:190]
            slug = base
            i = 1
            Model = self.__class__
            while Model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug

        super().save(*args, **kwargs)



# A garden is simply where a user stores their saved allotments
class Garden(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gardener")
    description = models.TextField(null=True, blank=True)
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

