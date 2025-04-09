from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SyllabusViewSet, LogBookViewSet

router = DefaultRouter()
router.register(r'syllabus', SyllabusViewSet)
router.register(r'logbook', LogBookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
]




