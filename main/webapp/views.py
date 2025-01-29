from django.shortcuts import render
import matplotlib

matplotlib.use("Agg")  # Para que Matplotlib no requiera una interfaz gráfica
import matplotlib.pyplot as plt
import io
import urllib
import base64


def index(request):
    return render(request, "index.html")


def graficar(request):
    grafico = None

    if request.method == "POST":
        try:
            # Obtener y procesar los valores de X e Y del formulario
            x_values = [
                float(x.strip()) for x in request.POST.get("x_values", "").split(",")
            ]
            y_values = [
                float(y.strip()) for y in request.POST.get("y_values", "").split(",")
            ]

            # Crear el gráfico
            plt.figure(figsize=(10, 6))
            plt.plot(x_values, y_values, "b-o")  # Línea azul con puntos
            plt.grid(True)
            plt.xlabel("Eje X")
            plt.ylabel("Eje Y")
            plt.title("Gráfico de valores X vs Y")

            # Guardar el gráfico en un buffer de memoria
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)

            # Codificar la imagen en base64
            image_png = buffer.getvalue()
            buffer.close()
            grafico = base64.b64encode(image_png).decode("utf-8")

            # Limpiar la figura actual de matplotlib
            plt.clf()

        except Exception as e:
            # Manejar errores (por ejemplo, valores no numéricos)
            grafico = None
            print(f"Error al generar el gráfico: {str(e)}")

    return render(request, "calculadora/graficar.html", {"plot_url": grafico})
