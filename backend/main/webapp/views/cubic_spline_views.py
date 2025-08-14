from django.shortcuts import render
from django.http import JsonResponse
from ..utils.cubic_spline import cubic_spline_method
import json

def cubic_spline(request):
    return render(request, 'cubic-spline.html')


def calculate_cubic_spline_view(request):
    try:
        points_json = request.GET.get("points")
        if not points_json:
            return JsonResponse({"error": "Falta el parámetro 'points'."})
        points = json.loads(points_json)
        x_interp = float(request.GET.get("x_interp"))
        boundary = request.GET.get("boundary", "natural")
        deriv_start = float(request.GET.get("deriv_start", 0))
        deriv_end = float(request.GET.get("deriv_end", 0))
        periodic_check = request.GET.get("periodic_check", "false").lower() == "true"

        result = cubic_spline_method(points, x_interp, boundary, deriv_start, deriv_end, periodic_check)
        print(result)
        return JsonResponse({"result": result})
    except Exception as e:
        return JsonResponse({"error": str(e)})