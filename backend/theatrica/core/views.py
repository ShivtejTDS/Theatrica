from rest_framework import viewsets
from .models import Syllabus, LogBook
from .serializers import SyllabusSerializer, LogBookSerializer
from rest_framework.permissions import IsAuthenticated

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsAuthenticated]


class LogBookViewSet(viewsets.ModelViewSet):
    queryset = LogBook.objects.all()
    serializer_class = LogBookSerializer
    permission_classes = [IsAuthenticated]
