from django.test import SimpleTestCase

SECTIONS = {
    "news": ["/news/", "/news/yellowsubmarine", "/news/2026", "/news/щось-там", "/news/12345", "/news/last-article"],
    "management": ["/management/", "/management/director", "/management/хтось", "/management/ceo/bio"],
    "about": ["/about/", "/about/history", "/about/team/2020", "/about/будь-який-текст", "/about/our-story/1991"],
    "contacts": ["/contacts/", "/contact/", "/contacts/map", "/contact/us", "/contacts/odesa/tairovo", "/contacts/odesa/office-sadova"],
}
TITLES = {"news": "Новини", "management": "Керівництво компанії", "about": "Про компанію", "contacts": "Контакти"}


class RoutingTest(SimpleTestCase):
    def test_home(self):
        self.assertContains(self.client.get("/"), "Ласкаво просимо")

    def test_sections_and_catch_all_show_their_section(self):
        for section, paths in SECTIONS.items():
            for path in paths:
                with self.subTest(path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, f"<h1>{TITLES[section]}</h1>", html=True)
                    self.assertTemplateUsed(response, f"{section}.html")
