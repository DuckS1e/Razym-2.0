from rest_framework import serializers
from .models import Users, Events, Leaderboard

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'email', 'full_name', 'role', 'city', 'age', 'is_approved']

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.full_name', read_only=True)
    class Meta:
        model = Events
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    class Meta:
        model = Leaderboard
        fields = '__all__'
