"""
URL configuration for the_giddy_gardener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import accounts_views

urlpatterns = [
    path('', include(('growing_projects.urls', 'growing_projects'), namespace='growing_projects')),          # site root handled by growing_projects (namespaced)
    path('admin/', admin.site.urls),
    # Override the login/signup routes so we can present a combined view
    path('accounts/login/', accounts_views.login_or_signup, name='account_login'),
    path('accounts/signup/', accounts_views.login_or_signup, name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('blogs/', include(('blog.urls','blog'), namespace='blog')),

]