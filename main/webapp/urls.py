from django.urls import path
from . import views

urlpatterns = [
    path("calculadora/", views.graficar, name="graficar"),
]
