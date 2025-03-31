from django.shortcuts import render
from django.http import JsonResponse
from ..utils.gauss_maximum_column_pivoting import gauss_maximum_column_pivoting_method
import json


def gauss_maximum_column_pivoting(request):
    return render(request, 'gauss_maximum_column_pivoting.html')


def calculate_gauss_maximum_column_pivoting(request):
    try:
        print("Start calculating gauss back substitution...")
        print(request)
    except Exception as error:
        print(error)
        return JsonResponse({'error': str(error)}, status=500)
