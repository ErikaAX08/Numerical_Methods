from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class MetodoHistorial(models.Model):
    METODOS_CHOICES = [
        ('biseccion', 'Bisección'),
        ('secante', 'Secante'),
        ('newton', 'Newton-Raphson'),
        ('regla falsa', 'Regla Falsa'),
        ('lagrange', 'Lagrange'),
        ('diferencias divididas', 'Divided differences'),
        ('neville', 'Neville'),
        ('eliminacion hacia atras', 'Gaussian elimination with back replacement'),
        ('pivoteo maximo columnas', 'Gaussian elimination with maximum column pivoting'),
        ('pivoteo escalado columna', 'Gaussian elimination with column-scaled pivoting'),
        ('factorizacion lu', 'Factorization LU'),
        ('trapecio', 'Trapecio simple'),
        ('trapecio compuesto', 'Trapecio compuesto'),
        ('simpson 1/3', 'Simpson 1/3'),
        ('simpson 1/3 compuesto', 'Simpson 1/3 compuesto'),
        ('simpson 3/8', 'Simpson 3/8'),
        ('simpson 3/8 compuesto', 'Simpson 3/8 compuesto'),
    ]
    
    metodo = models.CharField(max_length=50, choices=METODOS_CHOICES)
    funcion = models.TextField(blank=True, null=True)
    # Aquí puedes guardar cualquier cosa (valores, matrices, etc.)
    datos = models.JSONField()
    resultado = models.FloatField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metodo} - {self.fecha.date()}"


class TrapecioHistorial(models.Model):
    funcion = models.CharField(max_length=255)
    limite_inferior = models.FloatField()
    limite_superior = models.FloatField()
    subintervalos = models.IntegerField(default=1)
    resultado = models.FloatField()
    # Eliminamos el campo fecha_creacion que está causando problemas
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de cálculo de trapecio"
        verbose_name_plural = "Historial de cálculos de trapecio"

    def __str__(self):
        return f"∫({self.limite_inferior}, {self.limite_superior}) {self.funcion} dx = {self.resultado:.6f}"
    

class TrapecioCompuestoHistorial(models.Model):
    funcion = models.CharField(max_length=255)
    limite_inferior = models.FloatField()
    limite_superior = models.FloatField()
    subintervalos = models.IntegerField()
    resultado = models.FloatField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de cálculo de trapecio"
        verbose_name_plural = "Historial de cálculos de trapecio"

    def __str__(self):
        return f"∫({self.limite_inferior}, {self.limite_superior}), {self.subintervalos}, {self.funcion} dx = {self.resultado:.6f}"
