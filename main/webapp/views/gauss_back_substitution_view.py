from django.shortcuts import render
from django.http import JsonResponse
from ..utils.gauss_back_substitution import gauss_back_substitution_method
import json


def gauss_back_substitution(request):
    return render(request, 'gauss_back_substitution.html')


def calculate_gauss_back_substitution_view(request):
    try:
        print("Start calculating gauss back substitution...")
        print(request)
    except Exception as error:
        print(error)
        return JsonResponse({'error': str(error)}, status=500)
