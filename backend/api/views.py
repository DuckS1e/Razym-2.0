from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Events, Leaderboard, Users, EventParticipants, Feedback
from django.db.models import Count, Sum, Q

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
    """Страница организаторов (все пользователи с ролью 'organizer')"""
    organizers = Users.objects.filter(role='organizer').annotate(
        events_count=Count('organized_events'),
        total_participants=Sum('organized_events__participants')
    )
    return render(request, 'public.html', {
        'organizers': organizers,
    })

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
