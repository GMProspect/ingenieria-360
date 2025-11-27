from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    
    # Aquí está la magia de MongoDB: Guardamos un diccionario completo
    especificaciones = models.JSONField(default=dict, blank=True)
    
    cantidad = models.IntegerField(default=1)
    fecha_adquisicion = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"
