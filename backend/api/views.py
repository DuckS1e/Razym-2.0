from rest_framework import viewsets, permissions
from .models import Users, Events, Leaderboard, EventParticipants, Feedback
from .serializers import UserSerializer, EventSerializer, LeaderboardSerializer
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
def home_page(request):
    """Главная страница: список предстоящих мероприятий"""
    from django.utils import timezone
    upcoming_events = Events.objects.filter(
        status='published',
        date__gte=timezone.now()
    ).order_by('date')
    past_events = Events.objects.filter(
        status='published',
        date__lt=timezone.now()
    ).order_by('-date')[:5]
    return render(request, 'home.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

def leaderboard_page(request):
    """Таблица лидеров (топ-100)"""
    top_users = Leaderboard.objects.select_related('user').order_by('rank')[:100]
    return render(request, 'leaderboard.html', {
        'leaderboard': top_users,
    })

def organizers_page(request):
    organizers = Users.objects.filter(role='organizer').annotate(
        events_count=Count('organized_events'),
        total_participants=Count('organized_events__participants', distinct=True)
    ).prefetch_related('organizer_profile', 'received_feedback')
    return render(request, 'public.html', {'organizers': organizers})

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name', '')
    department = data.get('department', '')
    role = data.get('role', 'participant')

    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка, существует ли пользователь с таким email
    if Users.objects.filter(email=email).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = Users(
        email=email,
        full_name=full_name,
        city=department,
        role=role,
        password_hash=make_password(password),
        is_approved=True
    )
    user.save()

    from .models import ParticipantProfiles
    ParticipantProfiles.objects.create(user=user)

    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
@login_required
def profile_page(request):
    """Профиль текущего пользователя (участника)"""
    user = request.user
    participations = EventParticipants.objects.filter(user=user).select_related('event')
    leaderboard_entry = Leaderboard.objects.filter(user=user).first()
    organizer_profile = None
    if user.role == 'organizer':
        try:
            organizer_profile = user.organizer_profile
        except:
            pass
    return render(request, 'profile.html', {
        'user_profile': user,
        'participations': participations,
        'leaderboard_entry': leaderboard_entry,
        'organizer_profile': organizer_profile,
    })

@login_required
def admin_panel_page(request):
    """Панель администратора (только для пользователей с ролью admin или moderator)"""
    if request.user.role not in ['admin', 'moderator']:
        return render(request, '403.html', status=403)
    total_events = Events.objects.count()
    total_participants = Users.objects.filter(role='participant').count()
    total_organizers = Users.objects.filter(role='organizer').count()
    pending_organizers = Users.objects.filter(role='organizer', is_approved=False)
    return render(request, 'admin_panel.html', {
        'total_events': total_events,
        'total_participants': total_participants,
        'total_organizers': total_organizers,
        'pending_organizers': pending_organizers,
    })

class UserViewSet(viewsets.ModelViewSet):
    """API для работы с пользователями"""
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  

class EventViewSet(viewsets.ModelViewSet):
    """API для мероприятий"""
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """Только чтение для лидерборда"""
    queryset = Leaderboard.objects.all().order_by('rank')[:100]
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
