from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Contact, CVItem, CVProfile, CVSection


class OwnerAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_superuser:
            raise self.get_invalid_login_error()


class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = [
            "name", "headline", "email", "phone", "location",
            "linkedin_url", "github_url",
        ]
        labels = {
            "name": "Full name",
            "headline": "Professional headline",
            "email": "Email",
            "phone": "Phone",
            "location": "Location",
            "linkedin_url": "LinkedIn URL",
            "github_url": "GitHub URL",
        }
        widgets = {
            "headline": forms.TextInput(attrs={"placeholder": "Your role or professional headline"}),
        }


class CVSectionForm(forms.ModelForm):
    class Meta:
        model = CVSection
        fields = ["title", "icon", "order", "is_visible"]
        labels = {
            "title": "Section heading",
            "icon": "Heading icon",
            "order": "Position",
            "is_visible": "Show this section on the public CV",
        }


class CVItemForm(forms.ModelForm):
    class Meta:
        model = CVItem
        fields = [
            "icon", "title", "subtitle", "description", "details",
            "category", "proficiency", "order", "is_visible",
        ]
        labels = {
            "icon": "Item icon (optional)",
            "title": "Title",
            "subtitle": "Subtitle or date",
            "description": "Description",
            "details": "Bullet points",
            "category": "Group (for technical skills)",
            "proficiency": "Rating (0–100)",
            "order": "Position",
            "is_visible": "Show on the public CV",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "details": forms.Textarea(attrs={"rows": 5, "placeholder": "Write one point per line"}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'subject', 'message', 'consent',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].choices = [
            choice for choice in self.fields['subject'].choices
            if choice[0] not in {'college', 'lycee'}
        ]

    # ── Validation personnalisée ──────────────────────────────────────────────

    def clean_consent(self):
        """L'utilisateur doit obligatoirement cocher la case."""
        consent = self.cleaned_data.get('consent')
        if not consent:
            raise forms.ValidationError(
                "Vous devez accepter la politique de confidentialité pour continuer."
            )
        return consent

    def clean_phone(self):
        """Validation simple du format de téléphone marocain (optionnel)."""
        phone = (self.cleaned_data.get('phone') or '').strip()
        if phone and not phone.replace(' ', '').replace('+', '').isdigit():
            raise forms.ValidationError("Veuillez entrer un numéro de téléphone valide.")
        return phone