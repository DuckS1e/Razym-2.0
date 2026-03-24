from django.db import models

class Users(models.Model):
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    is_approved = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.full_name


class Events(models.Model):
    organizer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='organized_events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    complexity_coef = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'events'

    @property
    def category_name(self):
        return self.category or "Разное"


class EventPrizes(models.Model):
    event = models.ForeignKey(Events, models.CASCADE, related_name='prizes')
    prize_type = models.CharField(max_length=50)
    points = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'event_prizes'


class EventParticipants(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='event_participations')
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='participants')
    status = models.CharField(max_length=20)
    confirmation_method = models.CharField(max_length=10, blank=True, null=True)
    confirmed_by = models.ForeignKey(Users, models.SET_NULL, db_column='confirmed_by', related_name='confirmed_participations', blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    points_earned = models.IntegerField(blank=True, null=True)
    registered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'event_participants'


class Feedback(models.Model):
    event = models.ForeignKey(Events, models.CASCADE, related_name='feedback', blank=True, null=True)
    participant = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='given_feedback')
    organizer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='received_feedback')
    rating = models.SmallIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'


class Leaderboard(models.Model):
    user = models.OneToOneField(Users, models.CASCADE, primary_key=True)
    rank = models.IntegerField(blank=True, null=True)
    total_points = models.IntegerField(blank=True, null=True)
    category_breakdown = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'leaderboard'


class OrganizerProfiles(models.Model):
    user = models.OneToOneField(Users, models.CASCADE, primary_key=True)
    trust_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    events_count = models.IntegerField(blank=True, null=True)
    common_prizes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'organizer_profiles'


class ParticipantProfiles(models.Model):
    user = models.OneToOneField(Users, models.CASCADE, primary_key=True)
    total_points = models.IntegerField(blank=True, null=True)
    current_rank = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    points_to_next = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'participant_profiles'


class Settings(models.Model):
    key = models.CharField(primary_key=True, max_length=100)
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'settings'
