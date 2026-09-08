from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from .models import Contact
from .forms import ContactForm  # si tu veux utiliser le ModelForm

class ContactCreatview(CreateView):
    model = Contact
    form_class = ContactForm  # ou fields='__all__' si pas de forms.py
    template_name = "myApp/pages/contact.html"
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        messages.success(self.request, "Votre message a été envoyé avec succès ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs ci-dessous ❌")
        return super().form_invalid(form)


def home(request):
    return render(request,'myApp/pages/home.html')

def index(request):
    return render(request,'myApp/pages/about.html')

def accueil(request):
    return render(request,'myApp/pages/accueil.html')

def cv(request):
    return render(request,'myApp/pages/cv.html')