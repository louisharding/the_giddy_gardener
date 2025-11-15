from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Crop

# Create your views here.
class CropList(generic.ListView):
    queryset = Crop.objects.filter()
    template_name = "growing_projects/index.html"
    #how its paginated (default like 3, down by like 10, look into making it endless scrolling)


def crop_detail(request, name):
    """
    """
    queryset = Crop.objects.filter()
    crop = get_object_or_404(queryset, name=name)

    return render(
        request,
        "growing_projects/crop_profile.html",
        {
            "crop": crop,
        },
    )