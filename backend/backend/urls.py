"""
URL configuration for backend project.

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('leaderboard/', TemplateView.as_view(template_name='leaderboard.html'), name='leaderboard'),
    path('public/', TemplateView.as_view(template_name='public.html'), name='public'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('admin_panel/', TemplateView.as_view(template_name='admin_panel.html'), name='admin_panel'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('hello/', TemplateView.as_view(template_name='hello.html'), name='hello'),
]
