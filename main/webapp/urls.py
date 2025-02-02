from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("taylor-series/", views.taylor_series, name="taylor_series"),
    path("calculate-taylor/", views.calculate_taylor, name="calculate_taylor"),
    path("regula-falsi/", views.regula_falsi, name="regula_falsi"),
]
