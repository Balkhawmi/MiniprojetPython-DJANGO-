from time import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Employe(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_embauche = models.DateField()

    def clean(self):
        # Vérifier si la date d'embauche est dans le futur
        if self.date_embauche > timezone.now().date():
            raise ValidationError(_('La date d\'embauche ne peut pas être dans le futur.'))

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Dirigeant(models.Model):
    employe = models.OneToOneField(Employe, on_delete=models.CASCADE)
    droits_supplémentaires = models.BooleanField(default=True)

    def __str__(self):
        return f"Dirigeant: {self.employe.nom} {self.employe.prenom}"

class Conge(models.Model):
    TYPE_CONGE = (
        ('CP', 'Congé Payé'),
        ('RTT', 'Réduction du Temps de Travail'),
        ('MAL', 'Maladie'),
    )
    
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    type_conge = models.CharField(max_length=3, choices=TYPE_CONGE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    STATUT_CHOICES = [
        ('En_attente', 'En attente'),
        ('Approuve', 'Approuvé'),
        ('Refuse', 'Refusé'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='En_attente')

    def clean(self):
        if self.date_debut > self.date_fin:
            raise ValidationError(_('La date de début ne peut pas être postérieure à la date de fin.'))

    def __str__(self):
        return f"{self.type_conge} - {self.employe.nom} {self.employe.prenom}"
