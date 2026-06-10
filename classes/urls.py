from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatiereViewSet, CoursViewSet

router = DefaultRouter()
router.register('matieres', MatiereViewSet, basename='matiere')
router.register('cours', CoursViewSet, basename='cours')

urlpatterns = [path('', include(router.urls))]