from . import views
from django.urls import path, include

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('<slug:slug>/', views.post_detail, name='post_detail'), 
]