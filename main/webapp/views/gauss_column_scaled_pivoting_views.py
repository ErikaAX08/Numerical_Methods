from django.shortcuts import render
from django.http import JsonResponse
from ..utils.gauss_column_scaled_pivoting import gauss_column_scaled_pivoting_method
import json


def gauss_column_scaled_pivoting(request):
    return render(request, 'gauss-column-scaled-pivoting.html')


def calculate_gauss_column_scaled_pivoting(request):
    try:
        print("Start calculating gauss back substitution...")
        print(request)
    except Exception as error:
        print(error)
        return JsonResponse({'error': str(error)}, status=500)
