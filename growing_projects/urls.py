from django.urls import path, include
from . import views

app_name = 'growing_projects'

urlpatterns = [
    path('', views.home, name='home'),
    # app routes
    path('crops/', views.CropList.as_view(), name='crops'),
    path('crops/<slug:slug>/', views.crop_detail, name='crop_detail'),
    path('my-garden/', views.my_garden, name='my_garden'),
    
]