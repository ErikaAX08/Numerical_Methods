from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("calculadora/", views.graficar, name="graficar"),
]
