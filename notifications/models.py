from django.db import models
from accounts.models import Utilisateur


class Notification(models.Model):
    STATUT_CHOICES = [
        ('envoye', 'Envoyé'),
        ('lu', 'Lu'),
        ('en_attente', 'En attente'),
    ]

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    titre = models.CharField(max_length=255)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(
        max_length=15,
        choices=STATUT_CHOICES,
        default='en_attente'
    )
    type_notification = models.CharField(
        max_length=20,
        default='general'
    )

    class Meta:
        db_table = 'notifications'

    def __str__(self):
        return f"{self.titre} → {self.utilisateur}"