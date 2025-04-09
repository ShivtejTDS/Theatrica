from rest_framework import serializers
from .models import Syllabus, LogBook

class SyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = '__all__'


class LogBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogBook
        fields = '__all__'
