from django.urls import path
from .views.equations import BisectionView

urlpatterns = [
    path("equations/bisection", BisectionView.as_view(), name="bisection")
]
