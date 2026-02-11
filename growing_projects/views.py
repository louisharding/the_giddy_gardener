from .models import Garden, Crop
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
class CropList(generic.ListView):
    model = Crop
    template_name = "growing_projects/index.html"
    context_object_name = 'crop_list'
    paginate_by = 24

    def get_queryset(self):
        qs = super().get_queryset().order_by('common_name', 'scientific_name')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(common_name__icontains=q) | Q(scientific_name__icontains=q))
        crop_type = self.request.GET.get('type')
        if crop_type:
            qs = qs.filter(type=crop_type)
        life = self.request.GET.get('life_cycle')
        if life:
            qs = qs.filter(life_cycle=life)
        return qs


def crop_detail(request, slug):
    """Display a single Crop by slug."""
    queryset = Crop.objects.filter()
    # Try to resolve by slug first; if that fails, try by primary key (id).
    try:
        crop = queryset.get(slug=slug)
    except Crop.DoesNotExist:
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



# Delete a crop from the database - only for permitted users
@login_required
def crop_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseForbidden('Delete must be POST')
    crop = get_object_or_404(Crop, pk=pk)
    if not request.user.has_perm('growing_projects.delete_crop'):
        raise PermissionDenied
    crop.delete()
    return redirect('growing_projects:crops')



# A logged-in user can add a crop to their garden 
@login_required
def add_crop_to_garden(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")
    crop_id = request.POST.get('crop_id')
    if not crop_id:
        messages.error(request, "No crop specified.")
        return redirect('growing_projects:my_garden')
    try:
        crop = get_object_or_404(Crop, pk=int(crop_id))
    except ValueError:
        messages.error(request, "Invalid crop id.")
        return redirect('growing_projects:my_garden')

    garden, _ = Garden.objects.get_or_create(owner=request.user)
    if garden.crops.filter(pk=crop.pk).exists():
        messages.info(request, "That crop is already in your garden.")
    else:
        garden.crops.add(crop)
        messages.success(request, f"Added {crop.common_name or crop.scientific_name} to your garden.")
    return redirect('growing_projects:my_garden')

# A logged-in user can remove a crop from their garden
@login_required
def remove_crop_from_garden(request):
    """Handle POST to remove a crop from the current user's garden."""
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")
    crop_id = request.POST.get('crop_id')
    if not crop_id:
        messages.error(request, "No crop specified.")
        return redirect('growing_projects:my_garden')
    try:
        crop = Garden.objects.get(owner=request.user).crops.get(pk=int(crop_id))
    except (ValueError, Garden.DoesNotExist, Crop.DoesNotExist):
        messages.error(request, "Crop not found in your garden.")
        return redirect('growing_projects:my_garden')

    Garden.objects.get(owner=request.user).crops.remove(crop)
    messages.success(request, f"Removed {crop.common_name or crop.scientific_name}.")
    return redirect('growing_projects:my_garden')