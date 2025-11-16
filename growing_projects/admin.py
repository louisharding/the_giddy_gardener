from django.contrib import admin
from .models import Crop, Allotment, Garden


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
	list_display = ('common_name', 'scientific_name', 'slug', 'type')
	prepopulated_fields = {'slug': ('common_name',)}


@admin.register(Allotment)
class AllotmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'garden')


@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
	list_display = ('owner', 'description')
