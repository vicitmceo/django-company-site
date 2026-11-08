from django.test import SimpleTestCase


class ServicesTest(SimpleTestCase):
    def test_index(self):
        response = self.client.get("/services/")
        self.assertContains(response, "<h1>Послуги</h1>", html=True)

    def test_each_subsection(self):
        for slug, title in {"web": "Веб-розробка", "mobile": "Мобільні застосунки",
                            "ai": "ШІ та автоматизація", "support": "Підтримка та супровід"}.items():
            for path in (f"/services/{slug}", f"/services/{slug}/"):
                with self.subTest(path=path):
                    self.assertContains(self.client.get(path), f"<h1>{title}</h1>", html=True)

    def test_unknown_subpath_shows_index(self):
        self.assertTemplateUsed(self.client.get("/services/blockchain"), "services/index.html")
