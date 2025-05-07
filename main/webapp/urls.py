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
from .views.gauss_column_scaled_pivoting_views import gauss_column_scaled_pivoting, \
    calculate_gauss_column_scaled_pivoting
from .views.gauss_back_substitution_view import gauss_back_substitution, calculate_gauss_back_substitution_view
from .views.gauss_maximum_column_pivoting_views import gauss_maximum_column_pivoting, \
    calculate_gauss_maximum_column_pivoting
from .views.chulesky_factorization_view import chulesky_factorization, calculate_chulesky_factorization
from .views.lu_factorization_view import lu_factorization, calculate_lu_factorization
from .views.simpson_3_8_simple_views import simpson_3_8_simple_page, calculate_simpson_3_8_simple
from .views.trapecio_simple_views import trapecio_simple, calculate_trapezoid

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
    path("gauss-column-scaled-pivoting/", gauss_column_scaled_pivoting, name="gauss_column_scaled_pivoting"),
    path("calculate-gauss-column-scaled-pivoting/", calculate_gauss_column_scaled_pivoting,
         name="calculate_gauss_column_scaled_pivoting"),
    path("gauss_back_substitution/", gauss_back_substitution, name="gauss_back_substitution"),
    path("calculate_gauss_back_substitution/", calculate_gauss_back_substitution_view,
         name="calculate_gauss_back_substitution"),
    path("gauss-maximum-column-pivoting/", gauss_maximum_column_pivoting, name="gauss_maximum_column_pivoting"),
    path("calculate-gauss-maximum-column-pivoting/", calculate_gauss_maximum_column_pivoting,
         name="calculate_gauss_maximum_column_pivoting"),
    path("chulesky-factorization/", chulesky_factorization, name="chulesky_factorization"),
    path("calculate-chulesky-factorization/", calculate_chulesky_factorization,
         name="calculate_chulesky_factorization"),
    path("lu-factorization/", lu_factorization, name="lu_factorization"),
    path("calculate-lu-factorization/", calculate_lu_factorization,),
    path("simpson-3-8-simple/", simpson_3_8_simple_page, name="simpson_3_8_simple"),
    path("calculate-simpson-3-8-simple/", calculate_simpson_3_8_simple, name="calculate_simpson_3_8_simple"),
    path("calculate-lu-factorization/", calculate_lu_factorization,
         name="calculate_lu_factorization"),
    path("trapecio_simple/", trapecio_simple, name="trapecio_simple"),
    path("calculate_trapezoid/", calculate_trapezoid, name="calculate_trapezoid")
]
