from rest_framework import serializers
from .models import Employe, Dirigeant, Conge

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = '__all__'

    def validate_email(self, value):
        if Employe.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

class DirigeantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dirigeant
        fields = '__all__'

class CongeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conge
        fields = '__all__'
