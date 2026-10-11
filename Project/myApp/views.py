from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ContactForm, CVItemForm, CVProfileForm, CVSectionForm, OwnerAuthenticationForm
from .models import Contact, CVItem, CVProfile, CVSection

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


def index(request):
    return redirect("root")


def cv(request):
    sections = list(
        CVSection.objects.filter(is_visible=True)
        .prefetch_related("items")
    )
    for section in sections:
        section.visible_items = [
            item for item in section.items.all() if item.is_visible
        ]
        for item in section.visible_items:
            item.detail_lines = [line for line in item.details.splitlines() if line.strip()]
            if section.key in {"tools", "languages"}:
                filled_count = round(item.proficiency / 20)
                item.rating_dots = [index < filled_count for index in range(5)]
        if section.key == "skills":
            groups = {}
            for item in section.visible_items:
                groups.setdefault(item.category or "Other", []).append(item)
            section.skill_groups = [
                {"name": name, "items": items} for name, items in groups.items()
            ]

    profile = CVProfile.objects.first()
    return render(request, "myApp/pages/cv.html", {
        "profile": profile,
        "sections": sections,
    })


def owner_required(view):
    @wraps(view)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapped


class DashboardLoginView(LoginView):
    template_name = "myApp/dashboard/login.html"
    authentication_form = OwnerAuthenticationForm
    redirect_authenticated_user = True


class DashboardLogoutView(LogoutView):
    next_page = reverse_lazy("dashboard_login")


@owner_required
def dashboard_home(request):
    sections = CVSection.objects.all()
    return render(request, "myApp/dashboard/home.html", {
        "profile": CVProfile.objects.first(),
        "sections": sections,
    })


@owner_required
def dashboard_profile_edit(request):
    profile = CVProfile.objects.first()
    if profile is None:
        profile = CVProfile.objects.create()
    form = CVProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile details saved.")
        return redirect("dashboard_home")
    return render(request, "myApp/dashboard/form.html", {
        "form": form,
        "page_title": "Edit profile",
        "cancel_url": reverse_lazy("dashboard_home"),
    })


@owner_required
def dashboard_section(request, key):
    section = get_object_or_404(CVSection, key=key)
    items = section.items.all()
    return render(request, "myApp/dashboard/section.html", {
        "section": section,
        "items": items,
    })


@owner_required
def dashboard_section_edit(request, key):
    section = get_object_or_404(CVSection, key=key)
    form = CVSectionForm(request.POST or None, instance=section)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Section settings saved.")
        return redirect("dashboard_section", key=section.key)
    return render(request, "myApp/dashboard/form.html", {
        "form": form,
        "page_title": f"Edit {section.title}",
        "cancel_url": reverse_lazy("dashboard_section", kwargs={"key": section.key}),
    })


@owner_required
def dashboard_item_create(request, key):
    section = get_object_or_404(CVSection, key=key)
    form = CVItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.section = section
        if not item.order:
            item.order = (section.items.order_by("-order").values_list("order", flat=True).first() or 0) + 1
        item.save()
        messages.success(request, "CV item added.")
        return redirect("dashboard_section", key=section.key)
    return render(request, "myApp/dashboard/form.html", {
        "form": form,
        "page_title": f"Add to {section.title}",
        "cancel_url": reverse_lazy("dashboard_section", kwargs={"key": section.key}),
    })


@owner_required
def dashboard_item_edit(request, item_id):
    item = get_object_or_404(CVItem.objects.select_related("section"), pk=item_id)
    form = CVItemForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "CV item updated.")
        return redirect("dashboard_section", key=item.section.key)
    return render(request, "myApp/dashboard/form.html", {
        "form": form,
        "page_title": f"Edit {item.title}",
        "cancel_url": reverse_lazy("dashboard_section", kwargs={"key": item.section.key}),
    })


@owner_required
def dashboard_item_delete(request, item_id):
    item = get_object_or_404(CVItem.objects.select_related("section"), pk=item_id)
    if request.method == "POST":
        section_key = item.section.key
        item.delete()
        messages.success(request, "CV item deleted.")
        return redirect("dashboard_section", key=section_key)
    return render(request, "myApp/dashboard/confirm_delete.html", {
        "item": item,
        "cancel_url": reverse_lazy("dashboard_section", kwargs={"key": item.section.key}),
    })