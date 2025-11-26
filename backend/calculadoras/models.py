from django.db import models

class HistorialCalculo(models.Model):
    TIPO_CHOICES = [
        ('OHM', 'Ley de Ohm'),
        ('TRANSMISOR', 'Transmisor 4-20mA'),
        ('VIBRACION', 'Sonda de Vibración'),
        ('CONVERSOR', 'Conversor Universal'),
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    etiqueta = models.CharField(max_length=200, help_text="Ej: Bomba Principal")
    
    # Guardamos inputs y outputs como JSON para máxima flexibilidad
    datos_entrada = models.JSONField(default=dict)
    resultado = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.etiqueta} ({self.get_tipo_display()})"
