from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    ClasseListView,
    EtudiantsParClasseView,
    ListeUtilisateursView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user/', UserProfileView.as_view()),
    path('classes/', ClasseListView.as_view()),
    path('classes/<int:classe_id>/etudiants/', EtudiantsParClasseView.as_view()),
    path('utilisateurs/', ListeUtilisateursView.as_view()),
]