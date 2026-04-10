from django.db import models
from django.contrib.auth.models import User as DjangoUser
import random
import string

def generate_voucher():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


class Tournoi(models.Model):
    nom = models.CharField(max_length=100)
    jeu = models.CharField(max_length=100)
    date = models.DateField()
    heure = models.TimeField()
    participants = models.ManyToManyField(DjangoUser, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.jeu})"


class Reservation(models.Model):
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    motif = models.TextField()
    temps_secondes = models.IntegerField()

    # 🔥 LA LIGNE IMPORTANTE
    tournoi = models.ForeignKey(Tournoi, on_delete=models.SET_NULL, null=True, blank=True)

    voucher = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=generate_voucher
    )

    def __str__(self):
        return f"{self.user.username} - {self.temps_secondes}s"