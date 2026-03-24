from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Avg
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Users, Events, EventParticipants, Feedback, Leaderboard, Settings, OrganizerProfiles, ParticipantProfiles
from .serializers import (
    UserSerializer, EventSerializer, LeaderboardSerializer,
    EventParticipantSerializer, FeedbackSerializer, SettingsSerializer,
    CustomTokenObtainPairSerializer
)
from .permissions import IsAdminOrModerator
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import AccessToken

def home_page(request):
    upcoming_events = Events.objects.filter(status='published', date__gte=timezone.now()).order_by('date')
    past_events = Events.objects.filter(status='published', date__lt=timezone.now()).order_by('-date')[:5]
    return render(request, 'home.html', {'upcoming_events': upcoming_events, 'past_events': past_events})

def leaderboard_page(request):
    top_users = Leaderboard.objects.select_related('user').order_by('rank')[:100]
    return render(request, 'leaderboard.html', {'leaderboard': top_users})

def organizers_page(request):
    organizers = Users.objects.filter(role='organizer').annotate(
        events_count=Count('organized_events'),
        total_participants=Count('organized_events__participants', distinct=True)
    ).prefetch_related('organizer_profile', 'received_feedback')
    return render(request, 'public.html', {'organizers': organizers})

@login_required
def profile_page(request):
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

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name', '')
    department = data.get('department', '')
    role = data.get('role', 'participant')
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)
    if Users.objects.filter(email=email).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = Users(
        email=email,
        full_name=full_name,
        city=department,
        role=role,
        password_hash=make_password(password),
        is_approved=True if role != 'organizer' else False
    )
    user.save()
    if role == 'participant':
        ParticipantProfiles.objects.create(user=user)
    elif role == 'organizer':
        OrganizerProfiles.objects.create(user=user)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def register_for_event(request):
    event_id = request.data.get('event')
    if not event_id:
        return Response({'detail': 'event id required'}, status=status.HTTP_400_BAD_REQUEST)
    event = get_object_or_404(Events, id=event_id)
    if EventParticipants.objects.filter(user=request.user, event=event).exists():
        return Response({'detail': 'Already registered'}, status=status.HTTP_400_BAD_REQUEST)
    EventParticipants.objects.create(
        user=request.user,
        event=event,
        status='registered',
        registered_at=timezone.now()
    )
    return Response({'detail': 'Registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_feedback(request):
    organizer_id = request.data.get('organizer_id')
    rating = request.data.get('rating')
    comment = request.data.get('comment')
    if not organizer_id or not rating:
        return Response({'detail': 'organizer_id and rating required'}, status=status.HTTP_400_BAD_REQUEST)
    organizer = get_object_or_404(Users, id=organizer_id, role='organizer')
    Feedback.objects.create(
        participant=request.user,
        organizer=organizer,
        rating=rating,
        comment=comment,
        created_at=timezone.now()
    )
    avg_rating = Feedback.objects.filter(organizer=organizer).aggregate(avg=Avg('rating'))['avg']
    if avg_rating:
        organizer.organizer_profile.trust_rating = avg_rating
        organizer.organizer_profile.save()
    return Response({'detail': 'Feedback submitted'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_weights(request):
    if request.user.role not in ['admin', 'moderator']:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    for key, value in request.data.items():
        if key.startswith('weight_'):
            Settings.objects.update_or_create(key=key, defaults={'value': value})
    return Response({'detail': 'Weights saved'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_organizer(request, user_id):
    if request.user.role not in ['admin', 'moderator']:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(Users, id=user_id, role='organizer')
    user.is_approved = True
    user.save()
    return Response({'detail': 'Approved'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_organizer(request, user_id):
    if request.user.role not in ['admin', 'moderator']:
        return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(Users, id=user_id, role='organizer')
    user.delete()
    return Response({'detail': 'Rejected'})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def session_login(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = Users.objects.get(id=user_id)
        login(request, user)  # создаёт сессию
        return Response({'status': 'ok'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaderboard.objects.all().order_by('rank')[:100]
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
