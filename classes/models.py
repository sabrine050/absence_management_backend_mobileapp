from django.db import models
from accounts.models import Utilisateur, Classe


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'matieres'

    def __str__(self):
        return self.nom


class Cours(models.Model):
    JOURS = [
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
    ]

    nom = models.CharField(max_length=150)
    code_cours = models.CharField(max_length=20, blank=True, null=True)
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='cours_enseignes'
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='cours'
    )
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name='cours'
    )
    horaire_debut = models.TimeField(blank=True, null=True)
    horaire_fin = models.TimeField(blank=True, null=True)
    jour_semaine = models.CharField(
        max_length=10,
        choices=JOURS,
        blank=True, null=True
    )

    class Meta:
        db_table = 'cours'

    def __str__(self):
        return f"{self.nom} - {self.classe}"