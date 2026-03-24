# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActivityLog(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    event = models.ForeignKey('Events', models.DO_NOTHING, blank=True, null=True)
    points_change = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'activity_log'
        db_table_comment = 'История изменений баллов для графиков активности'


class EventCategories(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'event_categories'
        db_table_comment = 'Справочник категорий'


class EventCategoryLinks(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)  # The composite primary key (event_id, category_id) found, that is not supported. The first column is selected.
    category = models.ForeignKey(EventCategories, models.DO_NOTHING)

    class Meta:
        db_table = 'event_category_links'
        unique_together = (('event', 'category'),)
        db_table_comment = 'Связь мероприятий с категориями'


class EventParticipants(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    event = models.ForeignKey('Events', models.DO_NOTHING)
    status = models.CharField(max_length=20)
    confirmation_method = models.CharField(max_length=10, blank=True, null=True)
    confirmed_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='confirmed_by', related_name='eventparticipants_confirmed_by_set', blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    points_earned = models.IntegerField(blank=True, null=True)
    registered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'event_participants'
        db_table_comment = 'Участники мероприятий и их статус'


class EventPrizes(models.Model):
    event = models.ForeignKey('Events', models.DO_NOTHING)
    prize_type = models.CharField(max_length=50)
    points = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'event_prizes'
        db_table_comment = 'Призы, привязанные к мероприятиям'


class EventTags(models.Model):
    event = models.OneToOneField('Events', models.DO_NOTHING, primary_key=True)  # The composite primary key (event_id, tag_id) found, that is not supported. The first column is selected.
    tag = models.ForeignKey('Tags', models.DO_NOTHING)

    class Meta:
        db_table = 'event_tags'
        unique_together = (('event', 'tag'),)
        db_table_comment = 'Связь мероприятий с тегами'


class Events(models.Model):
    organizer = models.ForeignKey('Users', models.CASCADE, related_name='organized_events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    complexity_coef = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'events'
        db_table_comment = 'Мероприятия'


class Feedback(models.Model):
    event = models.ForeignKey(Events, models.DO_NOTHING)
    participant = models.ForeignKey('Users', models.DO_NOTHING)
    organizer = models.ForeignKey('Users', models.DO_NOTHING, related_name='feedback_organizer_set')
    rating = models.SmallIntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'feedback'
        db_table_comment = 'Отзывы участников на организаторов'


class Leaderboard(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    rank = models.IntegerField(blank=True, null=True)
    total_points = models.IntegerField(blank=True, null=True)
    category_breakdown = models.TextField(blank=True, null=True)  # This field type is a guess.
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'leaderboard'
        db_table_comment = 'Кэш топ-100 участников'


class OrganizerProfiles(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    trust_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    events_count = models.IntegerField(blank=True, null=True)
    common_prizes = models.TextField(blank=True, null=True)  # This field type is a guess.
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'organizer_profiles'
        db_table_comment = 'Дополнительная информация об организаторах'


class ParticipantProfiles(models.Model):
    user = models.OneToOneField('Users', models.DO_NOTHING, primary_key=True)
    total_points = models.IntegerField(blank=True, null=True)
    current_rank = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    points_to_next = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'participant_profiles'
        db_table_comment = 'Дополнительная информация об участниках'


class Settings(models.Model):
    key = models.CharField(primary_key=True, max_length=100)
    value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'settings'
        db_table_comment = 'Глобальные настройки системы'


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'tags'
        db_table_comment = 'Теги для облака тегов'


class Users(models.Model):
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    is_approved = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'users'
        db_table_comment = 'Все пользователи системы'
