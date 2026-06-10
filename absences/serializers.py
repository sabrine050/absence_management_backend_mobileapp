from rest_framework import serializers
from .models import Absence, Justification
from accounts.models import Utilisateur
from classes.models import Cours


class UtilisateurSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'nom', 'prenom', 'email', 'role']


class CoursSimpleSerializer(serializers.ModelSerializer):
    classe_nom = serializers.CharField(
        source='classe.nom', read_only=True
    )
    matiere_nom = serializers.CharField(
        source='matiere.nom', read_only=True
    )

    class Meta:
        model = Cours
        fields = [
            'id', 'nom', 'code_cours',
            'horaire_debut', 'horaire_fin',
            'jour_semaine', 'classe_nom', 'matiere_nom'
        ]


class JustificationSerializer(serializers.ModelSerializer):
    soumis_par_details = UtilisateurSimpleSerializer(
        source='soumis_par',
        read_only=True
    )

    class Meta:
        model = Justification
        fields = [
            'id',
            'absence',
            'soumis_par',
            'soumis_par_details',
            'date_soumission',
            'statut',
            'motif',
            'url_document',
            'commentaire_admin',
        ]
        # soumis_par est ajouté automatiquement dans la view
        read_only_fields = ['soumis_par', 'date_soumission']


class AbsenceSerializer(serializers.ModelSerializer):
    etudiant_details = UtilisateurSimpleSerializer(
        source='etudiant',
        read_only=True
    )
    cours_details = CoursSimpleSerializer(
        source='cours',
        read_only=True
    )
    justification = JustificationSerializer(read_only=True)

    etudiant_nom = serializers.CharField(
        source='etudiant.nom',
        read_only=True
    )
    etudiant_prenom = serializers.CharField(
        source='etudiant.prenom',
        read_only=True
    )

    class Meta:
        model = Absence
        fields = [
            'id',
            'etudiant',
            'etudiant_details',
            'etudiant_nom',
            'etudiant_prenom',
            'cours',
            'cours_details',
            'date_absence',
            'statut',
            'commentaire',
            'justification',
            'date_creation',
        ]