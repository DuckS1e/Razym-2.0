from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from . import views
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

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
    path('api/register/', views.register_user, name='api_register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/event_participants/', views.register_for_event, name='register_event'),
    path('api/feedback/', views.submit_feedback, name='feedback'),
    path('api/settings/', views.update_weights, name='weights'),
    path('api/users/<int:user_id>/approve/', views.approve_organizer, name='approve_organizer'),
    path('api/users/<int:user_id>/reject/', views.reject_organizer, name='reject_organizer'),
    
    path('', include(router.urls)),
]
