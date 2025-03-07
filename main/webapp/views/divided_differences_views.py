from django.shortcuts import render
from django.http import JsonResponse

def divided_differences(request):
    return render(request, 'divided-differences.html')