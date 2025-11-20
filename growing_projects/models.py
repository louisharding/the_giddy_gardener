from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

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
    ("ephemeral", "Ephemeral"),
)


# Could have a PICTURE field for the crop - makes perfect sense
# A crop is grown in an allotment. Crops have multiple properties and can only be effected by admins
class Crop(models.Model):
    scientific_name = models.CharField(max_length=200, unique=True, null=False, blank=True, default="")                 
    common_name = models.CharField(max_length=200, null=False, blank=True, default="")     
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=False, blank=True)                       
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    # Life cycle; how the crop grows, matures and yields throughout it's life
    life_cycle = models.CharField(max_length=50, choices=LIFE_CYCLE_CHOICES, null=True, blank=True)
    # Image for the crop (optional). Files stored under MEDIA_ROOT/crops/
    image = models.ImageField(upload_to='crops/', null=True, blank=True)
    # Sowing & Harvesting ranges; the earliest and latest a crop can be sown and harvested
    sowing_date_earliest = models.DateField(null=True, blank=True)
    sowing_date_latest = models.DateField(null=True, blank=True)
    harvesting_date_earliest = models.DateField(null=True, blank=True)
    harvesting_date_latest = models.DateField(null=True, blank=True)

    def __str__(self):
        # Return a human-friendly representation for admin and debugging
        if getattr(self, 'common_name', None) and getattr(self, 'scientific_name', None):
            return f"{self.common_name} ({self.scientific_name})"
        # Fallback to the default object representation if fields are missing
        return super().__str__()

    def get_absolute_url(self):
        return reverse('growing_projects:crop_detail', kwargs={'slug': self.slug})

    def ensure_common_name(self):
        """If `common_name` is empty, set it to the scientific name (or empty string)."""
        # common_name is allowed to be blank; if it's blank or whitespace use scientific_name
        if not (self.common_name and str(self.common_name).strip()):
            self.common_name = self.scientific_name or ""

    def save(self, *args, **kwargs):
        # Auto-generate slug from common_name if not provided
        # Ensure common_name is present for display and slug generation
        self.ensure_common_name()
        if not self.slug:
            base = f"{slugify(self.scientific_name)}-{self.life_cycle or ''}-{self.type or ''}"[:190]
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
    crops = models.ManyToManyField('Crop', blank=True, related_name='gardens')

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

