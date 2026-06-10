from django.contrib import admin
from .models import Absence, Justification


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'date_absence', 'cours', 'statut', 'date_creation']
    list_filter = ['statut', 'date_absence']
    search_fields = ['etudiant__nom', 'etudiant__prenom']


@admin.register(Justification)
class JustificationAdmin(admin.ModelAdmin):
    list_display = ['absence', 'soumis_par', 'statut', 'date_soumission']
    list_filter = ['statut']