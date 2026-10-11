from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Contact, CVItem, CVProfile, CVSection

class SetupTests(TestCase):
    def test_existing_pages_load(self):
        for path in ['/', '/cv', '/contact', '/admin/login/']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_public_navigation_is_cv_and_contact_only(self):
        for path in ["/", "/cv", "/contact"]:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, ">CV</a>")
                self.assertContains(response, ">Contact</a>")
                self.assertNotContains(response, ">Home</a>")
                self.assertNotContains(response, "/dashboard/login/")
        self.assertRedirects(self.client.get("/about"), "/")

    def test_dashboard_login_accepts_only_the_owner(self):
        get_user_model().objects.create_user(username="visitor", password="test-password")
        login_url = reverse("dashboard_login")
        response = self.client.post(login_url, {
            "username": "visitor", "password": "test-password",
        })
        self.assertContains(response, "The username or password was not accepted.")
        self.assertNotIn("_auth_user_id", self.client.session)

        owner = get_user_model().objects.create_superuser(
            username="owner", email="owner@example.com", password="test-password"
        )
        response = self.client.post(login_url, {
            "username": owner.username, "password": "test-password",
        })
        self.assertRedirects(response, reverse("dashboard_home"))

    def test_removed_home_page_returns_not_found(self):
        self.assertEqual(self.client.get('/home').status_code, 404)

    def test_cv_is_home_page_and_accueil_is_removed(self):
        self.assertContains(self.client.get('/'), 'ELHADI ABDELMOUNAIM')
        self.assertEqual(self.client.get('/accueil').status_code, 404)

    def test_cv_content_comes_from_database(self):
        section = CVSection.objects.get(key="projects")
        CVItem.objects.create(section=section, title="Database-powered project", order=99)
        response = self.client.get("/")
        self.assertContains(response, "Database-powered project")
        self.assertContains(response, 'class="cv-section"')

    def test_dashboard_is_private_and_owner_only(self):
        response = self.client.get(reverse("dashboard_home"))
        self.assertRedirects(
            response,
            f"{reverse('dashboard_login')}?next={reverse('dashboard_home')}",
        )
        self.assertEqual(self.client.get(reverse("dashboard_login")).status_code, 200)

        user = get_user_model().objects.create_user(username="visitor", password="test-password")
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse("dashboard_home")).status_code, 403)

    def test_owner_can_add_edit_and_delete_cv_items(self):
        owner = get_user_model().objects.create_superuser(
            username="owner", email="owner@example.com", password="test-password"
        )
        self.client.force_login(owner)
        self.assertEqual(self.client.get(reverse("dashboard_home")).status_code, 200)

        add_url = reverse("dashboard_item_create", args=["projects"])
        response = self.client.post(add_url, {
            "icon": "✨", "title": "Created from dashboard", "subtitle": "Test project",
            "description": "Managed without editing code.", "details": "First detail",
            "category": "", "proficiency": 80, "order": 99, "is_visible": "on",
        })
        self.assertRedirects(response, reverse("dashboard_section", args=["projects"]))
        item = CVItem.objects.get(title="Created from dashboard")
        self.assertContains(self.client.get("/"), "Created from dashboard")

        edit_url = reverse("dashboard_item_edit", args=[item.pk])
        self.client.post(edit_url, {
            "icon": "✨", "title": "Updated from dashboard", "subtitle": "Test project",
            "description": "Updated without editing code.", "details": "First detail",
            "category": "", "proficiency": 80, "order": 99, "is_visible": "on",
        })
        item.refresh_from_db()
        self.assertEqual(item.title, "Updated from dashboard")
        self.assertContains(self.client.get("/"), "Updated from dashboard")

        self.client.post(reverse("dashboard_item_delete", args=[item.pk]))
        self.assertFalse(CVItem.objects.filter(pk=item.pk).exists())
        self.assertNotContains(self.client.get("/"), "Updated from dashboard")

    def test_owner_can_edit_profile_and_section_visibility(self):
        owner = get_user_model().objects.create_superuser(
            username="owner", email="owner@example.com", password="test-password"
        )
        self.client.force_login(owner)
        self.client.post(reverse("dashboard_profile_edit"), {
            "name": "A New CV Name", "headline": "A new role",
            "email": "new@example.com", "phone": "", "location": "",
            "linkedin_url": "", "github_url": "",
        })
        self.assertEqual(CVProfile.objects.get().name, "A New CV Name")
        self.assertContains(self.client.get("/"), "A New CV Name")

        self.client.post(reverse("dashboard_section_edit", args=["languages"]), {
            "title": "My Languages", "icon": "🌍", "order": 5, "is_visible": "on",
        })
        self.assertContains(self.client.get("/"), "My Languages")
        self.client.post(reverse("dashboard_section_edit", args=["languages"]), {
            "title": "My Languages", "icon": "🌍", "order": 5,
        })
        self.assertNotContains(self.client.get("/"), "My Languages")
        self.assertNotContains(self.client.get("/"), "English")

    def test_contact_without_optional_phone(self):
        client = Client(enforce_csrf_checks=True)
        client.get('/contact')
        response = client.post('/contact', {
            'first_name': 'Setup',
            'last_name': 'Test',
            'email': 'setup@example.com',
            'phone': '',
            'subject': 'info',
            'message': 'Temporary verification.',
            'consent': 'on',
            'csrfmiddlewaretoken': client.cookies['csrftoken'].value,
        }, HTTP_HOST='setup.replit.dev', HTTP_ORIGIN='https://setup.replit.dev',
            HTTP_X_FORWARDED_PROTO='https')
        self.assertRedirects(response, '/contact', fetch_redirect_response=False)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().phone, '')

    def test_contact_requires_consent(self):
        response = self.client.post('/contact', {
            'first_name': 'Setup', 'last_name': 'Test',
            'email': 'setup@example.com', 'subject': 'info',
            'message': 'Temporary verification.',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)
        self.assertContains(response, 'Vous devez accepter')
