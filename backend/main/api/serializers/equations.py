from rest_framework import serializers # type: ignore

class BisectionSerializer(serializers.Serializer):
    a = serializers.FloatField()
    b = serializers.FloatField()
    tolerance = serializers.FloatField(default=1e-5)
    max_iterations = serializers.IntegerField(default=100)
    
    # La función puede enviarse como string (ej: "x**2-4")
    function = serializers.CharField()
