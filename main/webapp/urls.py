from django.urls import path
from .views.home_views import index
from .views.taylor_series_views import calculate_taylor, taylor_series
from .views.regula_falsi_views import calculate_falsi, regula_falsi

urlpatterns = [
    path("", index, name="index"),
    path("taylor-series/", taylor_series, name="taylor_series"),
    path("calculate-taylor/", calculate_taylor, name="calculate_taylor"),
    path("regula-falsi/", regula_falsi, name="regula_falsi"),
    path("calculate-falsi/", calculate_falsi, name="calculate_falsi"),
]