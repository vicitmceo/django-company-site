from django.test import TestCase

from .models import ContactMessage

VALID = {
    "name": "Олена Коваль",
    "email": "olena@example.com",
    "phone": "",
    "subject": "Запит на розробку сайту",
    "message": "Доброго дня! Хочемо замовити корпоративний сайт.",
}


class ContactFormPageTest(TestCase):
    def test_contact_page_shows_form_on_every_contacts_url(self):
        for path in ("/contacts/", "/contact/", "/contacts/map"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'name="subject"')
                self.assertContains(response, "csrfmiddlewaretoken")

    def test_valid_post_saves_message_and_redirects_with_success(self):
        response = self.client.post("/contacts/", VALID, follow=True)
        self.assertEqual(ContactMessage.objects.count(), 1)
        saved = ContactMessage.objects.get()
        self.assertEqual(saved.email, VALID["email"])
        self.assertContains(response, "Дякуємо!")

    def test_post_to_alternative_url_redirects_back_to_same_url(self):
        response = self.client.post("/contact/", VALID)
        self.assertRedirects(response, "/contact/#contact-form", fetch_redirect_response=False)

    def test_short_message_is_rejected(self):
        response = self.client.post("/contacts/", {**VALID, "message": "Привіт"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "щонайменше 20 символів")
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_invalid_email_is_rejected(self):
        response = self.client.post("/contacts/", {**VALID, "email": "не-пошта"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_required_fields_are_validated(self):
        response = self.client.post("/contacts/", {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Перевірте, будь ласка")
        self.assertEqual(ContactMessage.objects.count(), 0)
