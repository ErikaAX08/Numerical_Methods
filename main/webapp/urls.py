from django.urls import path
from .views.home_views import index
from .views.taylor_series_views import calculate_taylor, taylor_series
from .views.regula_falsi_views import calculate_falsi, regula_falsi
from .views.bisection_method_views import calculate_bisection_method, bisection_method
from .views.secant_method_view import calculate_secant_method, secant_method
from .views.newton_raphson_method_view import newton_raphson, calculate_newton_raphson
from .views.divided_differences_views import divided_differences, calculate_divided_differences

urlpatterns = [
    path("", index, name="index"),
    path("taylor-series/", taylor_series, name="taylor_series"),
    path("calculate-taylor/", calculate_taylor, name="calculate_taylor"),
    path("regula-falsi/", regula_falsi, name="regula_falsi"),
    path("calculate-falsi/", calculate_falsi, name="calculate_falsi"),
    path("bisection-method/", bisection_method, name="bisection_method"),
    path("calculate-bisection-method/", calculate_bisection_method, name="calculate_bisection_method"),
    path("secant-method/", secant_method, name="secant_method"),
    path("calculate-secant-method/", calculate_secant_method, name="calculate_secant_method"),
    path("newton-raphson-method/", newton_raphson, name="newton_raphson_method"),
    path("calculate-newton-raphson-method/", calculate_newton_raphson, name="calculate_newton_raphson_method"),
    path("divided-differences/", divided_differences, name="divided_differences"),
    path("calculate_divided_differences/", calculate_divided_differences, name="calculate_divided_differences")    
]
