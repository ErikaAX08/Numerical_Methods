from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.equations import BisectionSerializer
from methods.equations.bisection import bisection
import sympy as sp

class BisectionView(APIView):
    
    """
    MÉTODO POST
    {
        "function": "x**2 - 4",
        "a": 0,
        "b": 5,
        "tolerance": 0.0001,
        "max_iterations": 100
    }
    """    

    def post(self, request):
        serializer = BisectionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            expr = sp.sympify(data["function"])
            f = sp.lambdify("x", expr, "math")
            try:
                result = bisection(f, data["a"], data["b"], data["tolerance"], data["max_iterations"])
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
