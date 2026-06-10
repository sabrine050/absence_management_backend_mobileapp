from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Utilisateur, Classe
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UtilisateurSerializer,
    ClasseSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user': UtilisateurSerializer(user).data,
                    'message': 'Inscription réussie',
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user': UtilisateurSerializer(user).data,
                    'message': 'Connexion réussie',
                }
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response({'message': 'Déconnexion réussie'})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UtilisateurSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UtilisateurSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ClasseListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        classes = Classe.objects.all().order_by('nom')
        serializer = ClasseSerializer(classes, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Seul admin peut créer une classe
        if request.user.role != 'administrateur':
            return Response(
                {'error': 'Permission refusée'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ClasseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class EtudiantsParClasseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, classe_id):
        # Vérifier que la classe existe
        try:
            classe = Classe.objects.get(id=classe_id)
        except Classe.DoesNotExist:
            return Response(
                {'error': 'Classe introuvable'},
                status=status.HTTP_404_NOT_FOUND,
            )

        etudiants = Utilisateur.objects.filter(
            classe_id=classe_id,
            role='etudiant',
            is_active=True,
        ).order_by('nom')

        serializer = UtilisateurSerializer(etudiants, many=True)
        return Response(serializer.data)


class ListeUtilisateursView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Seul admin peut voir tous les utilisateurs
        if request.user.role != 'administrateur':
            return Response(
                {'error': 'Permission refusée'},
                status=status.HTTP_403_FORBIDDEN,
            )
        role = request.query_params.get('role')
        utilisateurs = Utilisateur.objects.filter(is_active=True)
        if role:
            utilisateurs = utilisateurs.filter(role=role)
        serializer = UtilisateurSerializer(utilisateurs, many=True)
        return Response(serializer.data)