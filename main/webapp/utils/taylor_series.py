import matplotlib

matplotlib.use("Agg")  # For use without display
import matplotlib.pyplot as plt

import plotly.graph_objects as go

import numpy as np
from sympy import symbols, exp, sin, cos, sinh, cosh, log, series, lambdify

from django.utils.translation import gettext as _
import io

x = symbols("x")


def functions(func, x_val):
    if func == "exp(x)":
        return float(exp(x).subs(x, x_val))
    elif func == "exp(-x)":
        return float(exp(-x).subs(x, x_val))
    elif func == "sin(x)":
        return float(sin(x).subs(x, x_val))
    elif func == "cos(x)":
        return float(cos(x).subs(x, x_val))
    elif func == "sinh(x)":
        return float(sinh(x).subs(x, x_val))
    elif func == "cosh(x)":
        return float(cosh(x).subs(x, x_val))
    elif func == "ln(1+x)":
        return float(log(1 + x).subs(x, x_val))


def taylor_approximation(func, x_val, degree):
    try:
        taylor = series(func, x, 0, degree + 1).removeO()
        return float(taylor.subs(x, x_val))
    except Exception as e:
        print(f"Error en taylor_approximation: {str(e)}")  # Debug
        raise e


def generate_graph(func, a, b, pt_num, degrees):
    try:
        x_values = np.linspace(a, b, pt_num)
        original_function = lambdify(x, func, "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)

        plt.figure()
        plt.plot(original_x_values, original_y_values, label=f"Original: {func}", color="black")

        all_taylor_values = []
        for degree in degrees:
            taylor_values = [taylor_approximation(func, i, degree) for i in x_values]
            all_taylor_values.append(taylor_values)
            plt.plot(x_values, taylor_values, label=_("Degree {degree}").format(degree=degree))

        plt.xlabel("X")
        plt.ylabel("f(x)")
        plt.title(_("Taylor approximation for {func}").format(func=func))
        plt.legend()
        plt.grid(True)

        plt.xlim(a, b)
        if str(func) in ["sin(x)", "cos(x)"]:
            plt.ylim(-1.1, 1.1)
        else:
            plt.ylim(original_y_values.min() - 0.1, original_y_values.max() + 0.1)

        plt.axvline(x=0, color='dodgerblue')
        plt.axhline(y=0, color='red')

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", dpi=300)
        plt.close()
        buffer.seek(0)

        return buffer
    except Exception as e:
        print(f"Error en generate_graph: {str(e)}")  # Debug
        raise e


def generate_interactive_graph(func, a, b, pt_num, degrees):
    try:
        x_values = np.linspace(a, b, pt_num)
        fig = go.Figure()

        original_function = lambdify(x, func, "numpy")
        original_x_values = np.linspace(a, b, 1000)
        original_y_values = original_function(original_x_values)

        fig.add_trace(
            go.Scatter(
                x=original_x_values,
                y=original_y_values,
                name=f"Original: {func}",
                line=dict(color='black', width=2)
            )
        )

        colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)',
                  'rgb(44, 160, 44)', 'rgb(214, 39, 40)',
                  'rgb(148, 103, 189)']

        for i, degree in enumerate(degrees):
            taylor_values = [taylor_approximation(func, i, degree) for i in x_values]

            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=taylor_values,
                    name=f"Degree {degree}",
                    line=dict(color=colors[i % len(colors)]),
                    visible=True
                )
            )

        fig.update_layout(
            title=f"Taylor Series Approximation for {func}",
            xaxis_title="x",
            yaxis_title="f(x)",
            hovermode='x unified',
            showlegend=True,
            sliders=[{
                'currentvalue': {"prefix": "Degree: "},
                'steps': [
                    {
                        'method': 'update',
                        'label': str(degree),
                        'args': [{'visible': [True] + [i <= j for j, d in enumerate(degrees)]},
                                 {'title': f'Taylor Series up to Degree {degree}'}],
                    } for i, degree in enumerate(degrees)
                ]
            }],
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {'frame': {'duration': 1000, 'redraw': True},
                                        'fromcurrent': True}]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                          'mode': 'immediate'}]
                    }
                ]
            }]
        )

        if str(func) in ["sin(x)", "cos(x)"]:
            fig.update_layout(yaxis_range=[-1.1, 1.1])
        else:
            fig.update_layout(
                yaxis_range=[
                    original_y_values.min() - 0.1,
                    original_y_values.max() + 0.1
                ]
            )

        fig.update_layout(xaxis_range=[a, b])

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        return fig.to_json()

    except Exception as e:
        print(f"Error in generate_interactive_graph: {str(e)}")
        raise e
