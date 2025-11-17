from .models import Garden, Crop
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import GardenAddCropForm  # below

# Create your views here.
class CropList(generic.ListView):
    queryset = Crop.objects.filter()
    template_name = "growing_projects/index.html"
    #how its paginated (default like 3, down by like 10, look into making it endless scrolling)


def crop_detail(request, slug):
    """Display a single Crop by slug."""
    queryset = Crop.objects.filter()
    crop = get_object_or_404(queryset, slug=slug)

    return render(request, "growing_projects/crop_profile.html", {"crop": crop})


def home(request):
    context = {
        # 'featured': Crop.objects.filter(... )[:3],
    }
    return render(request, 'growing_projects/home.html', context)


def my_garden(request):
    # Minimal placeholder view for the user's garden page
    garden = None
    if request.user.is_authenticated:
        # `gardener` is the related_name on Garden.owner; get the first garden if any
        try:
            garden = request.user.gardener.first()
        except Exception:
            garden = None

    return render(request, 'growing_projects/my_garden.html', {"garden": garden})




class MyGardenView(LoginRequiredMixin, TemplateView):
    template_name = 'growing_projects/my_garden.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        garden, _ = Garden.objects.get_or_create(owner=self.request.user)
        ctx['garden'] = garden
        ctx['crops'] = garden.crops.all()
        ctx['add_form'] = GardenAddCropForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = GardenAddCropForm(request.POST)
        if form.is_valid():
            crop = form.cleaned_data['crop']
            garden, _ = Garden.objects.get_or_create(owner=request.user)
            garden.crops.add(crop)
            return redirect('growing_projects:my_garden')
        ctx = self.get_context_data()
        ctx['add_form'] = form
        return self.render_to_response(ctx)




@login_required
def remove_crop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        crop = get_object_or_404(Crop, pk=crop_id)
        garden, _ = Garden.objects.get_or_create(owner=request.user)
        garden.crops.remove(crop)
    return redirect('growing_projects:my_garden')