from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Classe


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'niveau']
    search_fields = ['nom']


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ['email', 'nom', 'prenom', 'role', 'classe', 'is_active']
    list_filter = ['role', 'is_active', 'classe']
    search_fields = ['email', 'nom', 'prenom']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations', {'fields': ('nom', 'prenom', 'role', 'telephone', 'classe')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'role', 'password1', 'password2'),
        }),
    )