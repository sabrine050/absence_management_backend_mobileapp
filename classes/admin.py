from django.contrib import admin
from .models import Matiere, Cours


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom']
    search_fields = ['nom']


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ['nom', 'enseignant', 'classe', 'matiere', 'jour_semaine']
    list_filter = ['jour_semaine', 'classe']
    search_fields = ['nom']