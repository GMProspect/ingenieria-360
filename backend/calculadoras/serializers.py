from rest_framework import serializers
from .models import HistorialCalculo

class HistorialCalculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialCalculo
        fields = '__all__'
