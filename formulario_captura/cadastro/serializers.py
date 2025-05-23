from rest_framework import serializers
from .models import Consultor

class ConsultorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultor
        fields = ['id', 'consultorNome', 'consultorEmail']