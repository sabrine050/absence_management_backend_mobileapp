# 🎓 Gestion des Absences — Backend Django

API REST pour la gestion des absences scolaires.

## 📋 Technologies

- Python 3.12
- Django 6.0
- Django REST Framework 3.17
- PostgreSQL
- Token Authentication

## 🚀 Installation

### Prérequis
- Python 3.10+
- PostgreSQL
- pip

### Étapes

1. Cloner le projet
```bash
git clone https://github.com/votre_user/absence_backend.git
cd absence_backend
```

2. Créer l'environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer la base de données dans `config/settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Gestion_absence',
        'USER': 'postgres',
        'PASSWORD': 'your password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

5. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Créer un superuser
```bash
python manage.py createsuperuser
```

7. Lancer le serveur
```bash
python manage.py runserver 0.0.0.0:8000
```

## 📡 Endpoints API

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| POST | `/api/register/` | Inscription | ❌ |
| POST | `/api/login/` | Connexion | ❌ |
| POST | `/api/logout/` | Déconnexion | ✅ |
| GET | `/api/user/` | Profil | ✅ |
| GET | `/api/classes/` | Liste classes | ✅ |
| GET | `/api/classes/{id}/etudiants/` | Étudiants par classe | ✅ |
| GET/POST | `/api/absences/` | Absences | ✅ |
| GET | `/api/absences/dashboard_stats/` | Statistiques | ✅ |
| GET/POST | `/api/justifications/` | Justifications | ✅ |
| GET/POST | `/api/cours/` | Cours | ✅ |
| GET/POST | `/api/matieres/` | Matières | ✅ |
| GET | `/api/notifications/` | Notifications | ✅ |

## 👥 Rôles et Permissions

| Action | Étudiant | Enseignant | Admin |
|--------|----------|------------|-------|
| Voir ses absences | ✅ | ✅ toutes | ✅ toutes |
| Créer une absence | ❌ | ✅ | ✅ |
| Modifier une absence | ❌ | ✅ | ✅ |
| Supprimer une absence | ❌ | ❌ | ✅ |
| Justifier ses absences | ✅ | ✅ | ✅ |
| Approuver justification | ❌ | ✅ | ✅ |

## 📸 Screenshots

### Admin Django
![Admin](screenshots/admin.png)

### API REST
![API](screenshots/api.png)
