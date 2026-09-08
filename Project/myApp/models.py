from django.db import models

class Contact(models.Model):

    SUJET_CHOICES = [
        ('info', "Demande d'information"),
        ('inscription', 'Inscription aux cours'),
        ('college', 'Cours niveau Collège'),
        ('lycee', 'Cours niveau Lycée'),
        ('tarifs', 'Tarifs'),
        ('autre', 'Autre sujet'),
    ]

    NIVEAU_CHOICES = [
        ('1app', '1ère Année Collège'),
        ('2app', '2ème Année Collège'),
        ('3app', '3ème Année Collège'),
        ('tc', 'Tronc Commun'),
        ('1bac', '1ère Bac'),
        ('2bac', '2ème Bac'),
    ]

    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=20, blank=True, null=True)

    subject = models.CharField(
        max_length=20,
        choices=SUJET_CHOICES
    )

    niveau = models.CharField(
        max_length=10,
        choices=NIVEAU_CHOICES,
        blank=True,
        null=True
    )

    message = models.TextField()

    consent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"