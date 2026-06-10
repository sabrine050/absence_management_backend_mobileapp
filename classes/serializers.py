from rest_framework import serializers
from .models import Matiere, Cours
from accounts.serializers import UtilisateurSerializer, ClasseSerializer


class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'description']


class CoursSerializer(serializers.ModelSerializer):
    enseignant_details = UtilisateurSerializer(
        source='enseignant', read_only=True
    )
    classe_details = ClasseSerializer(
        source='classe', read_only=True
    )
    matiere_details = MatiereSerializer(
        source='matiere', read_only=True
    )

    class Meta:
        model = Cours
        fields = [
            'id', 'nom', 'code_cours',
            'enseignant', 'enseignant_details',
            'classe', 'classe_details',
            'matiere', 'matiere_details',
            'horaire_debut', 'horaire_fin', 'jour_semaine'
        ]