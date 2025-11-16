from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('plants', views.CropList.as_view(), name='plants'),
    # path('<name:name>/', views.crop_detail, name='crop_detail'),
    #path for garden
]