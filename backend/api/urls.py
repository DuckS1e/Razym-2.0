from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from . import views
from .views import CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'leaderboard', views.LeaderboardViewSet)

urlpatterns = [
    path('', views.home_page, name='home'),
    path('leaderboard/', views.leaderboard_page, name='leaderboard'),
    path('organizers/', views.organizers_page, name='organizers'),
    path('profile/', views.profile_page, name='profile'),
    path('admin_panel/', views.admin_panel_page, name='admin_panel'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('hello/', TemplateView.as_view(template_name='hello.html'), name='hello'),
    path('register/', views.register_user, name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    
]
