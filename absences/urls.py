from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AbsenceViewSet, JustificationViewSet

router = DefaultRouter()
router.register('absences', AbsenceViewSet, basename='absence')
router.register('justifications', JustificationViewSet, basename='justification')

urlpatterns = [path('', include(router.urls))]