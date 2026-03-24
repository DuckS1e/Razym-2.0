from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'leaderboard', views.LeaderboardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
