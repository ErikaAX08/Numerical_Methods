from django.shortcuts import render
from django.http import JsonResponse

def neville_method(request):
    return render(request, 'neville_method.html')