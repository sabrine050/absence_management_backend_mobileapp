from django.db import models
from accounts.models import Utilisateur
from classes.models import Cours


class Absence(models.Model):
    STATUT_CHOICES = [
        ('absent', 'Absent'),
        ('present', 'Présent'),
        ('justifie', 'Justifié'),
        ('retard', 'Retard'),
    ]

    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='absences'
    )
    date_absence = models.DateField()
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='absences'
    )
    statut = models.CharField(
        max_length=15,
        choices=STATUT_CHOICES,
        default='absent'
    )
    commentaire = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'absences'

    def __str__(self):
        return f"{self.etudiant} - {self.date_absence} - {self.statut}"


class Justification(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
    ]

    absence = models.OneToOneField(
        Absence,
        on_delete=models.CASCADE,
        related_name='justification'
    )
    soumis_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='justifications_soumises'
    )
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=15,
        choices=STATUT_CHOICES,
        default='en_attente'
    )
    motif = models.CharField(max_length=255, blank=True, null=True)
    url_document = models.FileField(
        upload_to='justifications/',
        blank=True, null=True
    )
    commentaire_admin = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'justifications'

    def __str__(self):
        return f"Justification - {self.absence}"