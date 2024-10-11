from rest_framework import serializers
from .models import Employe, Dirigeant, Conge
from django.utils import timezone

class EmployeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employe
        fields = ['id', 'nom', 'prenom', 'poste', 'email', 'date_embauche']

    def validate_nom(self, value):
        if not value:
            raise serializers.ValidationError("Le nom est obligatoire.")
        return value

    def validate_prenom(self, value):
        if not value:
            raise serializers.ValidationError("Le prénom est obligatoire.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("L'email est obligatoire.")
        if Employe.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def validate_date_embauche(self, value):
        if not value:
            raise serializers.ValidationError("La date d'embauche est obligatoire.")
        if value > timezone.now().date():
            raise serializers.ValidationError("La date d'embauche ne peut pas être dans le futur.")
        return value

    def validate(self, data):
        # Créer une instance d'Employe pour appeler la méthode clean
        employe = Employe(**data)
        employe.clean()  # Appeler la méthode clean pour valider
        return data


class DirigeantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dirigeant
        fields = '__all__'


class CongeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conge
        fields = ['id','employe', 'type_conge', 'date_debut', 'date_fin', 'statut']

    def validate_type_conge(self, value):
        if value not in dict(Conge.TYPE_CONGE).keys():
            raise serializers.ValidationError("Type de congé invalide.")
        return value

    def validate_date_debut(self, value):
        if not value:
            raise serializers.ValidationError("La date de début est obligatoire.")
        return value

    def validate_date_fin(self, value):
        if not value:
            raise serializers.ValidationError("La date de fin est obligatoire.")
        return value

    def validate(self, data):
        # Vérifier que la date de début n'est pas postérieure à la date de fin
        if data['date_debut'] > data['date_fin']:
            raise serializers.ValidationError("La date de début ne peut pas être postérieure à la date de fin.")
        return data

    def create(self, validated_data):
        # Si 'statut' n'est pas fourni, il utilisera la valeur par défaut du modèle
        statut = validated_data.get('statut', 'En_attente')
        validated_data['statut'] = statut
        return super().create(validated_data)
