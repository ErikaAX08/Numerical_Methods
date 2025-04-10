import json
from django.shortcuts import render
from django.http import JsonResponse

from ..utils.lagrange import lagrange_method

def calculate_lu_factorization(request):
    print("Calculating LU factorization")


def lu_factorization(request):
    return render(request, 'lu_factorization.html')
