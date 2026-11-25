from company_site.tests import SeededTestCase

from .models import NewsArticle, Photo, Project, Service, TeamMember
from .templatetags.company_filters import eur, initials


class ServicesTest(SeededTestCase):
    def test_index_lists_services_from_db(self):
        response = self.client.get("/services/")
        self.assertContains(response, "<h1>Послуги</h1>", html=True)
        self.assertEqual(len(response.context["services"]), Service.objects.count())

    def test_each_subsection(self):
        for slug, title in {"web": "Веб-розробка", "mobile": "Мобільні застосунки",
                            "ai": "ШІ та автоматизація", "support": "Підтримка та супровід"}.items():
            for path in (f"/services/{slug}", f"/services/{slug}/"):
                with self.subTest(path=path):
                    self.assertContains(self.client.get(path), f"<h1>{title}</h1>", html=True)

    def test_db_only_service_has_its_own_page(self):
        self.assertContains(self.client.get("/services/crm"), "<h1>CRM-системи</h1>", html=True)

    def test_unknown_subpath_shows_index(self):
        self.assertTemplateUsed(self.client.get("/services/no-such-service"), "services/index.html")


class SeedTest(SeededTestCase):
    def test_every_table_has_20_to_30_rows(self):
        for model in (Service, Project, NewsArticle, TeamMember, Photo):
            with self.subTest(model=model.__name__):
                self.assertTrue(20 <= model.objects.count() <= 30)

    def test_images_are_stored_in_media(self):
        from django.conf import settings
        from pathlib import Path
        for obj in (Service.objects.first(), Project.objects.first(), NewsArticle.objects.first(),
                    TeamMember.objects.first(), Photo.objects.first()):
            field = obj.photo if isinstance(obj, TeamMember) else obj.image
            self.assertTrue((Path(settings.MEDIA_ROOT) / field.name).is_file())

    def test_seed_is_idempotent_without_reset(self):
        from django.core.management import call_command
        call_command("seed", verbosity=0)
        self.assertEqual(Service.objects.count(), 25)


class PagesFromDbTest(SeededTestCase):
    def test_home_context_has_custom_class_collections(self):
        response = self.client.get("/")
        page = response.context["page"]
        self.assertEqual(type(page["stats"][0]).__name__, "Stat")
        self.assertEqual(type(page["sections"][0]).__name__, "SectionLink")
        self.assertContains(response, "проєктів")

    def test_news_management_about_use_db_rows(self):
        self.assertEqual(len(self.client.get("/news/").context["articles"]), 25)
        self.assertEqual(len(self.client.get("/management/").context["members"]), 25)
        self.assertEqual(len(self.client.get("/about/").context["projects"]), 6)


class FilterTest(SeededTestCase):
    def test_eur(self):
        self.assertEqual(eur(1500), "1 500 €")
        self.assertEqual(eur("bad"), "")

    def test_initials(self):
        self.assertEqual(initials("Олена Коваль"), "ОК")


class SearchTest(SeededTestCase):
    def test_finds_service_case_insensitively_for_cyrillic(self):
        for q in ("веб", "ВЕБ", "Веб-розробка"):
            with self.subTest(q=q):
                response = self.client.get("/search/", {"q": q})
                titles = [s.title for s in response.context["results"].services]
                self.assertIn("Веб-розробка", titles)
                self.assertContains(response, "знайдено")

    def test_finds_news_and_projects(self):
        results = self.client.get("/search/", {"q": "Відні"}).context["results"]
        self.assertTrue(results.news)
        projects = self.client.get("/search/", {"q": "Зернотрейд"}).context["results"].projects
        self.assertEqual(len(projects), 1)

    def test_nothing_found_shows_message(self):
        response = self.client.get("/search/", {"q": "qwertyuiop"})
        self.assertContains(response, "нічого не знайдено")
        self.assertEqual(response.context["results"].total, 0)

    def test_empty_and_too_short_queries(self):
        self.assertContains(self.client.get("/search/"), "Введіть назву")
        self.assertContains(self.client.get("/search/", {"q": "в"}), "закороткий")

    def test_query_is_escaped(self):
        response = self.client.get("/search/", {"q": "<script>alert(1)</script>"})
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_header_has_search_form_on_every_page(self):
        self.assertContains(self.client.get("/about/"), 'action="/search/"')
