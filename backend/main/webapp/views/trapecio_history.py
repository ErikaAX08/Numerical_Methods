from django.http import JsonResponse
from webapp.models import TrapecioHistorial


def trapezoid_history(request):
    """
    Vista para obtener el historial de cálculos del trapecio.
    Devuelve JSON en lugar de HTML.
    """
    try:
        # Obtener los últimos 10 registros del historial
        history = TrapecioHistorial.objects.all().order_by('-id')[:10]

        # Preparar datos para JSON
        history_data = []
        for item in history:
            # Verificar si el modelo tiene el campo fecha_creacion
            if hasattr(item, 'fecha_creacion'):
                fecha = item.fecha_creacion.isoformat() if item.fecha_creacion else None
            else:
                fecha = None

            history_data.append({
                'id': item.id,
                'funcion': item.funcion,
                'limite_inferior': item.limite_inferior,
                'limite_superior': item.limite_superior,
                'subintervalos': item.subintervalos,
                'resultado': item.resultado,
                'fecha_creacion': fecha
            })

        # Devolver JSON con los datos del historial
        return JsonResponse(history_data, safe=False)

    except Exception as e:
        # Capturar cualquier error y devolverlo como JSON
        return JsonResponse({'error': str(e)}, status=500)
