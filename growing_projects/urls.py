from django.urls import path, include
from . import views

app_name = 'growing_projects'

urlpatterns = [
    path('', views.home, name='home'),
    # app routes
    path('crops/', views.CropList.as_view(), name='crops'),
    path('crops/<slug:slug>/', views.crop_detail, name='crop_detail'),
    path('crops/<int:pk>/edit/', views.crop_edit, name='crop_edit'),
    path('crops/<int:pk>/delete/', views.crop_delete, name='crop_delete'),
    path('my-garden/', views.my_garden, name='my_garden'),

]
    
