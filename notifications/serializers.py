from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'utilisateur', 'titre', 'message',
            'date_envoi', 'date_lecture',
            'statut', 'type_notification'
        ]