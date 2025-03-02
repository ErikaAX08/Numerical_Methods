from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
from ..utils.divided_differences import divided_differences_method


def calculate_divided_differences(x, y):
    """Calcula la tabla de diferencias divididas."""
    n = len(x)
    coef = np.zeros([n, n])
    coef[:, 0] = y

    for j in range(1, n):
        for i in range(n-j):
            coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x[i+j] - x[i])

    return coef


def evaluar_polinomio(coef, x_datos, x_eval):
    """Evalúa el polinomio interpolador en un punto x_eval."""
    n = len(x_datos)
    p = coef[0][0]
    for i in range(1, n):
        factor = 1
        for j in range(i):
            factor *= (x_eval - x_datos[j])
        p += coef[0][i] * factor
    return p

# Suponiendo que ya tienes una vista llamada 'metodos_numericos_view' o similar


def tu_vista_actual(request):
    # Mantén tu código existente aquí

    # Añade la lógica para diferencias divididas
    if request.method == 'POST':
        # Verificar si estamos procesando el formulario de diferencias divididas
        if 'calcular_diferencias' in request.POST:
            # Aquí procesarías los datos ingresados:
            # 1. Extraer los valores x e y de la solicitud
            x_valores = [float(x) for x in request.POST.get(
                'x_valores', '').split(',')]
            y_valores = [float(y) for y in request.POST.get(
                'y_valores', '').split(',')]

            # 2. Obtener el grado del polinomio y los puntos seleccionados
            grado = int(request.POST.get('grado', 1))
            indices = [int(idx)
                       for idx in request.POST.getlist('puntos_seleccionados')]

            # Verificar que se seleccionaron suficientes puntos
            if len(indices) != grado + 1:
                context['error'] = f"Debe seleccionar exactamente {grado+1} puntos para un polinomio de grado {grado}"
                return render(request, 'tu_template.html', context)

            # 3. Crear subconjuntos con los puntos seleccionados
            x_selec = [x_valores[i] for i in indices]
            y_selec = [y_valores[i] for i in indices]

            # 4. Calcular los coeficientes
            coef = calculate_divided_differences(x_selec, y_selec)

            # 5. Calcular el valor interpolado
            x_interpolar = float(request.POST.get('x_interpolar', 0))
            resultado = evaluar_polinomio(coef, x_selec, x_interpolar)

            # 6. Añadir resultados al contexto
            context = {
                'resultado_interpolacion': resultado,
                'x_interpolar': x_interpolar,
                'puntos_seleccionados': list(zip(x_selec, y_selec)),
                # Incluye otras variables de contexto que necesites
            }

def divided_differences(request):
    return render(request, 'divided-differences.html')