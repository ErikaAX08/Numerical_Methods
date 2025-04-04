from django.urls import path

from .views.gauss_maximum_column_pivoting_views import gauss_maximum_column_pivoting
from .views.home_views import index
from .views.taylor_series_views import calculate_taylor, taylor_series
from .views.regula_falsi_views import calculate_falsi, regula_falsi
from .views.bisection_method_views import calculate_bisection_method, bisection_method
from .views.secant_method_view import calculate_secant_method, secant_method
from .views.newton_raphson_method_view import newton_raphson, calculate_newton_raphson
from .views.divided_differences_views import divided_differences
from .views.neville_method_views import neville_method
from .views.cubic_spline_views import cubic_spline, calculate_cubic_spline_view
from .views.lagrange_views import lagrange, calculate_lagrange
from .views.gauss_maximum_column_pivoting_views import gauss_maximum_column_pivoting, \
    calculate_gauss_maximum_column_pivoting

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
    path("lagrange/", lagrange, name="lagrange"),
    path("calculate-lagrange/", calculate_lagrange, name="calculate_lagrange"),
    path("divided-differences/", divided_differences, name="divided_differences"),
    path("neville-method/", neville_method, name="neville_method"),
    path("cubic-spline/", cubic_spline, name="cubic_spline"),
    path("calculate-cubic-spline/", calculate_cubic_spline_view, name="calculate_cubic_spline"),
    path("gauss-maximum-column-pivoting/", gauss_maximum_column_pivoting, name="gauss_maximum_column_pivoting"),
    path("calculate-gauss-maximum-column-pivoting/", calculate_gauss_maximum_column_pivoting,
         name="calculate_gauss_maximum_column_pivoting"),
]
