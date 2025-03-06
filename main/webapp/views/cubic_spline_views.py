from django.shortcuts import render
from django.http import JsonResponse


def cubic_spline(request):
    return render(request, 'cubic-spline.html')
