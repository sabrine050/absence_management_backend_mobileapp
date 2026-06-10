from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils import timezone
from .models import Absence, Justification
from .serializers import AbsenceSerializer, JustificationSerializer


class EstEnseignantOuAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['enseignant', 'administrateur']


class EstProprietaire(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['enseignant', 'administrateur']:
            return True
        return obj.etudiant == request.user


class AbsenceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AbsenceSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Absence.objects.all().select_related(
            'etudiant', 'cours', 'cours__classe', 'cours__matiere'
        ).order_by('-date_absence')

        if user.role == 'etudiant':
            queryset = queryset.filter(etudiant=user)

        date = self.request.query_params.get('date')
        classe_id = self.request.query_params.get('classe_id')
        statut = self.request.query_params.get('statut')

        if date:
            queryset = queryset.filter(date_absence=date)
        if classe_id:
            queryset = queryset.filter(cours__classe_id=classe_id)
        if statut:
            queryset = queryset.filter(statut=statut)

        return queryset

    def create(self, request, *args, **kwargs):
        if request.user.role not in ['enseignant', 'administrateur']:
            return Response(
                {'error': 'Vous n\'avez pas la permission de créer une absence'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['enseignant', 'administrateur']:
            return Response(
                {'error': 'Vous n\'avez pas la permission de modifier une absence'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.role not in ['enseignant', 'administrateur']:
            return Response(
                {'error': 'Permission refusée'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'administrateur':
            return Response(
                {'error': 'Seul un administrateur peut supprimer une absence'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        now = timezone.now()
        queryset = self.get_queryset()

        absences_mois = queryset.filter(
            date_absence__year=now.year,
            date_absence__month=now.month
        )

        total = absences_mois.count()
        justifies = absences_mois.filter(statut='justifie').count()
        non_justifies = absences_mois.filter(statut='absent').count()
        retards = absences_mois.filter(statut='retard').count()

        recent = AbsenceSerializer(
            queryset[:10], many=True
        ).data

        return Response({
            'monthly_stats': {
                'total': total,
                'justified': justifies,
                'unjustified': non_justifies,
                'retards': retards,
            },
            'recent_absences': recent,
        })


class JustificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JustificationSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['enseignant', 'administrateur']:
            return Justification.objects.all().select_related(
                'absence__etudiant'
            )
        return Justification.objects.filter(
            absence__etudiant=user
        ).select_related('absence__etudiant')

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.role == 'etudiant':
            absence_id = request.data.get('absence')
            try:
                absence = Absence.objects.get(id=absence_id)
                if absence.etudiant != user:
                    return Response(
                        {'error': 'Vous ne pouvez justifier que vos propres absences'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Absence.DoesNotExist:
                return Response(
                    {'error': 'Absence introuvable'},
                    status=status.HTTP_404_NOT_FOUND
                )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            justification = serializer.save(soumis_par=request.user)
            absence = justification.absence
            absence.statut = 'justifie'
            absence.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        if request.user.role not in ['enseignant', 'administrateur']:
            return Response(
                {'error': 'Permission refusée'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.role not in ['enseignant', 'administrateur']:
            return Response(
                {'error': 'Permission refusée'},
                status=status.HTTP_403_FORBIDDEN
            )

        justification = self.get_object()
        nouveau_statut = request.data.get('statut')

        if nouveau_statut == 'approuve':
            justification.absence.statut = 'justifie'
            justification.absence.save()
        elif nouveau_statut == 'rejete':
            justification.absence.statut = 'absent'
            justification.absence.save()

        serializer = self.get_serializer(
            justification,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)