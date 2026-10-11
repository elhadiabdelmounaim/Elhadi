from django.test import Client, TestCase
from .models import Contact

class SetupTests(TestCase):
    def test_existing_pages_load(self):
        for path in ['/', '/accueil', '/about', '/cv', '/contact', '/admin/login/']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_removed_home_page_returns_not_found(self):
        self.assertEqual(self.client.get('/home').status_code, 404)

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
