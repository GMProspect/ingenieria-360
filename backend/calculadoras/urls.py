from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HistorialCalculoViewSet

router = DefaultRouter()
router.register(r'history', HistorialCalculoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
