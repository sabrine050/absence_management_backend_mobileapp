# 📱 Gestion des Absences — Frontend Flutter

Application mobile/web pour la gestion des absences scolaires construite avec Flutter et connectée à une API Django REST.

## 📋 Technologies

- Flutter 3.x
- Dart 3.x
- HTTP pour les appels API
- SharedPreferences pour le stockage local
- FilePicker pour l'upload de documents

## 🚀 Installation

### Prérequis
- Flutter SDK 3.0+
- Dart 3.0+
- Android Studio ou VS Code
- Backend Django démarré → [absence_backend](https://github.com/votre_user/absence_backend)

### Étapes

1. Cloner le projet
```bash
git clone https://github.com/votre_user/absence_frontend.git
cd absence_frontend
```

2. Installer les dépendances
```bash
flutter pub get
```

3. Configurer l'URL de l'API dans `lib/config/api_config.dart`
```dart
class ApiConfig {
  // ← Remplacer par votre IP locale (ipconfig sur Windows)
  static const String yourIp = 'VOTRE_IP';

  static String get baseUrl => 'http://$yourIp:8000/api';

  static List<String> get fallbackUrls => [
    'http://$yourIp:8000/api',   // Vrai téléphone
    'http://10.0.2.2:8000/api',  // Émulateur Android
    'http://localhost:8000/api',  // Chrome
    'http://127.0.0.1:8000/api',
  ];
}
```

4. Lancer l'application
```bash
# Chrome
flutter run -d chrome --web-browser-flag "--disable-web-security"

# Android
flutter run -d android

# iOS
flutter run -d ios
```

## 📱 Fonctionnalités

### 👨‍🏫 Enseignant
- ✅ Tableau de bord avec statistiques mensuelles
- ✅ Ajouter une absence par classe/étudiant/cours
- ✅ Voir toutes les absences
- ✅ Approuver/Rejeter les justifications

### 👨‍🎓 Étudiant
- ✅ Tableau de bord personnel
- ✅ Voir ses propres absences uniquement
- ✅ Justifier une absence avec document (PDF/JPG/PNG)
- ✅ Suivre le statut de ses justifications

### 👨‍💼 Administrateur
- ✅ Accès complet à toutes les fonctionnalités
- ✅ Gestion via Admin Django


## 🗂️ Structure du projet

```
lib/
├── config/
│   └── api_config.dart        # ← Configuration URLs API
├── components/
│   ├── add_absence.dart       # Formulaire ajout absence
│   ├── home.dart              # Dashboard principal
│   ├── justify_absence.dart   # Formulaire justification
│   ├── login.dart             # Connexion
│   ├── MainScreen.dart        # Onboarding
│   ├── register.dart          # Inscription
│   └── splash_screen.dart     # Splash screen
└── services/
    ├── auth_service.dart      # Login, Register, Profil
    └── absence_service.dart   # Absences, Justifications
```

## 📦 Dépendances `pubspec.yaml`

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  shared_preferences: ^2.2.0
  file_picker: ^6.0.0
  intl: ^0.18.0
```

## 👥 Comptes de test

| Rôle | Email            | Mot de passe                |
|------|------------------|-----------------------------|
| Administrateur | admin@test.com   | admin1234                   |
| Enseignant | .......@.....com | .....      (make a new one) |
| Étudiant | ......@......com | ......        (make a new one)               |

## 🔐 Permissions par rôle

| Action | Étudiant | Enseignant | Admin |
|--------|----------|------------|-------|
| Voir ses absences | ✅ | ✅ toutes | ✅ toutes |
| Ajouter une absence | ❌ | ✅ | ✅ |
| Justifier une absence | ✅ | ✅ | ✅ |
| Approuver/Rejeter | ❌ | ✅ | ✅ |
| Supprimer une absence | ❌ | ❌ | ✅ |

## ⚠️ Notes importantes

- Le backend Django doit être démarré avant de lancer l'app
- Sur Chrome utilisez `--disable-web-security` pour éviter les erreurs CORS
- Trouvez votre IP locale avec `ipconfig` sur Windows ou `ifconfig` sur Mac/Linux
- Les fichiers uploadés sont limités à 5MB (PDF, JPG, PNG)

## 🔗 Liens

- 🔗 [Backend Django](https://github.com/sabrine050/absence_management_backend_mobileapp)
- 📖 [Documentation Flutter](https://flutter.dev/docs)
- 📖 [Documentation Django REST](https://www.django-rest-framework.org/)

## 👨‍💻 Auteur

**Sabrine**
- GitHub: (https://github.com/sabrine050)
