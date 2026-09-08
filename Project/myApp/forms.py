from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

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
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and not phone.replace(' ', '').replace('+', '').isdigit():
            raise forms.ValidationError("Veuillez entrer un numéro de téléphone valide.")
        return phone