from django.shortcuts import render
from django.http import JsonResponse

def calculate_lagrange(request):
    print("calculating lagrange")


def lagrange(request):
    return render(request, 'lagrange.html')
