from django.shortcuts import render
from django.http import JsonResponse
from ..utils.gauss_column_scaled_pivoting import gauss_column_scaled_pivoting_method
import json
from django.views.decorators.csrf import csrf_exempt


def chulesky_factorization(request):
    return render(request, 'chulesky-factorization.html')


@csrf_exempt
def calculate_chulesky_factorization(request):
    print("Start calculating chulesky factorization")
