from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Matiere, Cours
from .serializers import MatiereSerializer, CoursSerializer


class MatiereViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MatiereSerializer

    def get_queryset(self):
        queryset = Matiere.objects.all()

        # Filtrer par classe si demandé
        # GET /api/matieres/?classe_id=1
        classe_id = self.request.query_params.get('classe_id')
        if classe_id:
            # Matières des cours de cette classe
            queryset = queryset.filter(
                cours__classe_id=classe_id
            ).distinct()

        return queryset


class CoursViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CoursSerializer

    def get_queryset(self):
        queryset = Cours.objects.all().select_related(
            'enseignant', 'classe', 'matiere'
        )

        # GET /api/cours/?classe_id=1
        classe_id = self.request.query_params.get('classe_id')
        if classe_id:
            queryset = queryset.filter(classe_id=classe_id)

        # GET /api/cours/?jour=lundi
        jour = self.request.query_params.get('jour')
        if jour:
            queryset = queryset.filter(jour_semaine=jour)

        return queryset

    # GET /api/cours/1/matieres/
    @action(detail=True, methods=['get'])
    def matieres(self, request, pk=None):
        cours = self.get_object()
        serializer = MatiereSerializer(cours.matiere)
        return Response(serializer.data)