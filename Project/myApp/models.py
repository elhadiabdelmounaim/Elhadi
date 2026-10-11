from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CVProfile(models.Model):
    name = models.CharField(max_length=160, blank=True)
    headline = models.CharField(max_length=240, blank=True)
    email = models.CharField(max_length=240, blank=True)
    phone = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=160, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "CV profile"
        verbose_name_plural = "CV profile"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class CVSection(models.Model):
    SECTION_KEYS = [
        ("about", "About Me"),
        ("education", "Academic Background"),
        ("skills", "Technical Skills"),
        ("projects", "Projects"),
        ("tools", "Programming Languages & Tools"),
        ("languages", "Languages"),
        ("certifications", "Certifications & Training"),
        ("soft_skills", "Soft Skills"),
    ]

    key = models.CharField(max_length=32, choices=SECTION_KEYS, unique=True)
    title = models.CharField(max_length=160)
    icon = models.CharField(max_length=16, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class CVItem(models.Model):
    section = models.ForeignKey(CVSection, on_delete=models.CASCADE, related_name="items")
    icon = models.CharField(max_length=16, blank=True)
    title = models.CharField(max_length=240)
    subtitle = models.CharField(max_length=240, blank=True)
    description = models.TextField(blank=True)
    details = models.TextField(
        blank=True,
        help_text="Optional: one bullet point per line.",
    )
    category = models.CharField(max_length=160, blank=True)
    proficiency = models.PositiveSmallIntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="0–100. Used for skill bars and language/tool rating dots.",
    )
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "CV item"
        verbose_name_plural = "CV items"

    def __str__(self):
        return self.title

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