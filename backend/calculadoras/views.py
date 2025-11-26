from rest_framework import viewsets
from .models import HistorialCalculo
from .serializers import HistorialCalculoSerializer

class HistorialCalculoViewSet(viewsets.ModelViewSet):
    queryset = HistorialCalculo.objects.all().order_by('-created_at')
    serializer_class = HistorialCalculoSerializer
