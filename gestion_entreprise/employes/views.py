from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from .models import Employe, Dirigeant, Conge
from .serializers import EmployeSerializer, DirigeantSerializer, CongeSerializer
from .permissions import IsDirigeant

class EmployeViewSet(viewsets.ModelViewSet):
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        """
        Restreindre la liste des employés à l'utilisateur actuel si l'utilisateur n'est pas un dirigeant.
        Les dirigeants peuvent voir tous les employés.
        """
        queryset = super().get_queryset()
       # Filtrer par poste
        poste = self.request.query_params.get('poste')
        if poste:
            queryset = queryset.filter(poste__icontains=poste)

        # Filtrer par date d'embauche
        date_embauche = self.request.query_params.get('date_embauche')
        if date_embauche:
            queryset = queryset.filter(date_embauche=date_embauche)

        # Restriction pour les utilisateurs non dirigeants
        if not self.request.user.groups.filter(name='Dirigeant').exists():
            queryset = queryset.filter(id=self.request.user.id)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Seuls les dirigeants peuvent créer de nouveaux employés.
        """
        if not request.user.groups.filter(name='Dirigeant').exists():
            return Response({'detail': 'Permission denied. Only dirigeants can create employees.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class DirigeantViewSet(viewsets.ModelViewSet):
    queryset = Dirigeant.objects.all()
    serializer_class = DirigeantSerializer
    permission_classes = [IsAuthenticated, IsDirigeant]

    def get_queryset(self):
        """
        Filtrer les dirigeants pour s'assurer que seuls les dirigeants peuvent lister d'autres dirigeants.
        """
        return super().get_queryset()

class CongeViewSet(viewsets.ModelViewSet):
    queryset = Conge.objects.all()
    serializer_class = CongeSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        """
        Les employés ne peuvent voir que leurs propres demandes de congé.
        Les dirigeants peuvent voir toutes les demandes de congé.
        """
        queryset = super().get_queryset()

         # Filtrer par employé
        employe_id = self.request.query_params.get('employe_id')
        if employe_id:
            queryset = queryset.filter(employe_id=employe_id)

        # Filtrer par type de congé
        type_conge = self.request.query_params.get('type_conge')
        if type_conge:
            queryset = queryset.filter(type_conge=type_conge)

        # Filtrer par statut
        statut = self.request.query_params.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)

        # Restriction pour les employés non dirigeants
        if not self.request.user.groups.filter(name='Dirigeant').exists():
            try:
                employe = Employe.objects.get(user=self.request.user)
                queryset = queryset.filter(employe=employe)
            except Employe.DoesNotExist:
                queryset = queryset.none()

        return queryset

    def update(self, request, *args, **kwargs):
        """
        Restreindre la modification à la mise à jour du champ statut uniquement pour les dirigeants.
        """
        if not request.user.groups.filter(name='Dirigeant').exists():
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        # Charger l'instance existante
        conge = self.get_object()

        # Ne mettre à jour que le champ "statut"
        data = {'statut': request.data.get('statut')}
        
        # Valider et sauvegarder uniquement le statut
        serializer = self.get_serializer(conge, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Restreindre la suppression des congés aux dirigeants uniquement.
        """
        if not request.user.groups.filter(name='Dirigeant').exists():
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
