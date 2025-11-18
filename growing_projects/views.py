from .models import Garden, Crop
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.http import Http404
from django.views import generic

from django.contrib.auth.decorators import login_required


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
        try:
            crop = queryset.get(pk=slug)
        except (Crop.DoesNotExist, ValueError):
            raise Http404("Crop does not exist")

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


def crop_edit(request, pk):
    """Minimal edit redirect: send user to Django admin change form if available, otherwise go back to detail."""
    crop = get_object_or_404(Crop, pk=pk)
    if not request.user.is_authenticated or not request.user.has_perm('growing_projects.change_crop'):
        raise PermissionDenied
    try:
        admin_url = reverse('admin:growing_projects_crop_change', args=[crop.pk])
        return redirect(admin_url)
    except Exception:
        return redirect('growing_projects:crop_detail', slug=crop.slug or crop.pk)


@login_required
def crop_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseForbidden('Delete must be POST')
    crop = get_object_or_404(Crop, pk=pk)
    if not request.user.has_perm('growing_projects.delete_crop'):
        raise PermissionDenied
    crop.delete()
    return redirect('growing_projects:crops')






@login_required
def remove_crop(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        crop = get_object_or_404(Crop, pk=crop_id)
        garden, _ = Garden.objects.get_or_create(owner=request.user)
        garden.crops.remove(crop)
    return redirect('growing_projects:my_garden')