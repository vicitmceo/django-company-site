"""Наповнює БД демо-даними (по 25 рядків у кожній таблиці) і генерує зображення в media/."""
import colorsys
import io
from datetime import date, timedelta

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw

from services.models import NewsArticle, Photo, Project, Service, TeamMember

SERVICES = [
    ("web", "Веб-розробка", 1500), ("mobile", "Мобільні застосунки", 3000),
    ("ai", "ШІ та автоматизація", 2000), ("support", "Підтримка та супровід", 300),
    ("ui-ux", "UI/UX дизайн", 900), ("crm", "CRM-системи", 2500),
    ("ecommerce", "Інтернет-магазини", 2200), ("cloud", "Хмарна інфраструктура", 1200),
    ("devops", "DevOps та CI/CD", 1400), ("security", "Кібербезпека", 1800),
    ("analytics", "Бізнес-аналітика", 1600), ("bi", "BI-дашборди", 1300),
    ("seo", "SEO-просування", 500), ("marketing", "Цифровий маркетинг", 700),
    ("testing", "Тестування та QA", 800), ("audit", "Технічний аудит", 600),
    ("migration", "Міграція даних", 1100), ("integration", "Інтеграції та API", 1000),
    ("chatbots", "Чат-боти", 900), ("ml", "Машинне навчання", 3500),
    ("erp", "ERP-рішення", 4000), ("iot", "IoT-рішення", 2800),
    ("web3", "Блокчейн-рішення", 3200), ("training", "Навчання команд", 400),
    ("consulting", "ІТ-консалтинг", 350),
]
CLIENTS = [
    "Зернотрейд", "АгроЛогіст", "ТеплоДім", "Карпатська аптека", "СмакБуд", "МедПлюс", "ЕкоЛайн",
    "ФінЕкспрес", "Світло-Енерго", "ЛьвівТранс", "ПростоБанк", "Дніпро-Сервіс", "ОсвітаОнлайн",
    "Туристичний світ", "БудМайстер", "Цифрова Пошта", "ЮрКонсалт", "Книгарня «Лист»", "СпортЗона",
    "ВінТех", "Полтава-Продукт", "Одеса-Порт", "Харків-Софт", "Київ-Авто", "Чернігів-Меблі",
]
PROJECT_KINDS = ["Корпоративний сайт", "Мобільний застосунок", "Чат-бот підтримки", "Інтернет-магазин",
                 "Панель аналітики"]
NEWS = [
    ("Продукт", "Запуск нової версії платформи"), ("Компанія", "Відкрито офіс у Відні"),
    ("Ювілей", "Нам 10 років"), ("ШІ", "Новий напрям: ШІ та автоматизація"),
    ("Події", "Виступ на ІТ-конференції у Києві"), ("Команда", "Стартувала програма стажувань"),
    ("Продукт", "Оновлено мобільний застосунок"), ("Компанія", "Нагорода за найкращий вебпроєкт року"),
    ("Події", "Мітап для розробників у Львові"), ("ШІ", "Чат-бот скоротив час відповіді вдвічі"),
    ("Команда", "До команди приєдналися п'ять нових інженерів"), ("Продукт", "Нова панель аналітики"),
    ("Компанія", "Партнерство з європейським банком"), ("Події", "Вебінар про кібербезпеку"),
    ("ШІ", "Запуск внутрішнього асистента для підтримки"), ("Команда", "День відкритих дверей в офісі"),
    ("Продукт", "Редизайн особистого кабінету клієнта"), ("Компанія", "Сертифікація за ISO 27001"),
    ("Події", "Хакатон для студентів"), ("ШІ", "Прогнозування попиту для роздрібної мережі"),
    ("Команда", "Корпоративне навчання з хмарних технологій"), ("Продукт", "Інтеграція з платіжними сервісами"),
    ("Компанія", "Новий дата-центр у Європі"), ("Події", "Участь у виставці цифрових рішень"),
    ("Команда", "Підсумки року: ми зросли до 80 фахівців"),
]
FIRST = ["Олександр", "Марія", "Андрій", "Ірина", "Дмитро", "Олена", "Тарас", "Наталія", "Богдан", "Юлія",
         "Сергій", "Вікторія", "Максим", "Анна", "Роман", "Оксана", "Павло", "Софія", "Артем", "Катерина",
         "Володимир", "Людмила", "Євген", "Тетяна", "Микола"]
LAST = ["Коваленко", "Шевчук", "Мельник", "Бойко", "Ткаченко", "Кравчук", "Олійник", "Шевченко", "Поліщук",
        "Лисенко", "Мороз", "Савчук", "Бондаренко", "Гончар", "Руденко", "Павленко", "Кузьменко", "Мартинюк",
        "Данильчук", "Остапчук", "Яремчук", "Левченко", "Попович", "Гриценко", "Білик"]
POSITIONS = [
    ("Генеральний директор", "Керівництво"), ("Технічний директор", "Керівництво"),
    ("Директор з розвитку", "Керівництво"), ("Фінансовий директор", "Керівництво"),
    ("Керівник відділу розробки", "Розробка"), ("Backend-розробник", "Розробка"),
    ("Frontend-розробник", "Розробка"), ("Мобільний розробник", "Розробка"),
    ("Дизайнер інтерфейсів", "Дизайн"), ("QA-інженер", "Якість"),
    ("DevOps-інженер", "Інфраструктура"), ("Аналітик даних", "Аналітика"),
    ("Проєктний менеджер", "Менеджмент"), ("HR-менеджер", "Персонал"),
]
PHOTO_TITLES = [
    "Командний вечір", "Офіс у Києві", "Вид з вікна", "Конференція", "Хакатон", "Мітап", "Обід у кафе",
    "Новий офіс", "Презентація продукту", "Робочий день", "Корпоратив", "Вручення нагород", "Стажери",
    "Ранкова кава", "Брейнстормінг", "Запуск проєкту", "Дошка планування", "Зустріч з клієнтом",
    "Вебінар", "Подарунки команді", "Спортивний день", "Підсумки року",
]


def make_image(index: int, size=(480, 320)) -> ContentFile:
    """Генерує кольорове зображення-заглушку (градієнт + фігури) і повертає як JPEG."""
    hue = (index * 0.137) % 1.0
    top = tuple(int(c * 255) for c in colorsys.hsv_to_rgb(hue, 0.55, 0.95))
    bottom = tuple(int(c * 255) for c in colorsys.hsv_to_rgb((hue + 0.08) % 1.0, 0.75, 0.55))
    width, height = size
    img = Image.new("RGB", size)
    draw = ImageDraw.Draw(img)
    for y in range(height):
        k = y / height
        draw.line([(0, y), (width, y)], fill=tuple(int(t + (b - t) * k) for t, b in zip(top, bottom)))
    shape = tuple(int(c * 255) for c in colorsys.hsv_to_rgb((hue + 0.5) % 1.0, 0.25, 1.0))
    cx, cy = width * (0.25 + 0.5 * ((index * 7) % 10) / 10), height * 0.4
    draw.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), fill=shape)
    draw.rectangle((0, height * 0.72, width, height), fill=(28, 36, 52))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=78)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Заповнює БД демо-даними (по 25 рядків у таблиці) та створює зображення в media/"

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Видалити наявні дані й створити заново")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self._clear()
        elif Service.objects.exists():
            self.stdout.write("Дані вже є. Запустіть з --reset, щоб створити заново.")
            return

        services = self._services()
        self._projects(services)
        self._news()
        self._team()
        self._photos()
        self.stdout.write(self.style.SUCCESS(
            f"Готово: послуг {Service.objects.count()}, проєктів {Project.objects.count()}, "
            f"новин {NewsArticle.objects.count()}, співробітників {TeamMember.objects.count()}, "
            f"фото {Photo.objects.count()}"))

    def _clear(self):
        for model, field in ((Photo, "image"), (TeamMember, "photo"), (NewsArticle, "image"),
                             (Project, "image"), (Service, "image")):
            for obj in model.objects.all():
                getattr(obj, field).delete(save=False)
            model.objects.all().delete()

    def _services(self):
        result = []
        for i, (slug, title, price) in enumerate(SERVICES):
            points = "\n".join([
                f"Аналіз вимог та планування: {title.lower()}",
                "Проєктування та розробка під ключ",
                "Тестування, запуск і навчання команди",
                "Підтримка та супровід після релізу",
            ])
            service = Service(slug=slug, title=title, price_from=price, points=points,
                              summary=f"{title}: від ідеї та прототипу до запуску й підтримки.")
            service.image.save(f"{slug}.jpg", make_image(i), save=False)
            service.save()
            result.append(service)
        return result

    def _projects(self, services):
        for i, client in enumerate(CLIENTS):
            kind = PROJECT_KINDS[i % len(PROJECT_KINDS)]
            project = Project(
                title=f"{kind} для «{client}»", client=client, year=2018 + i % 9,
                description=f"{kind} для компанії «{client}»: аналіз, дизайн, розробка та запуск за 3–6 місяців.",
                service=services[i % len(services)])
            project.image.save(f"project-{i + 1}.jpg", make_image(i + 30), save=False)
            project.save()

    def _news(self):
        start = date(2026, 11, 12)
        for i, (category, title) in enumerate(NEWS):
            article = NewsArticle(
                title=title, category=category, published_at=start - timedelta(days=9 * i),
                summary=f"{title}. Коротко про головне з життя компанії «Обрій».",
                body=f"{title}.\n\nДетальніше про цю подію розповідають наші фахівці. "
                     "Ми й надалі розвиваємо продукти та команду, щоб бізнес бачив далі.")
            article.image.save(f"news-{i + 1}.jpg", make_image(i + 60), save=False)
            article.save()

    def _team(self):
        for i, (first, last) in enumerate(zip(FIRST, LAST)):
            position, department = POSITIONS[i % len(POSITIONS)]
            member = TeamMember(
                full_name=f"{first} {last}", position=position, department=department,
                email=f"user{i + 1}@obriy.example",
                bio=f"{position} у компанії «Обрій». Працює над продуктами для клієнтів в Україні та Європі.")
            member.photo.save(f"member-{i + 1}.jpg", make_image(i + 90, (320, 320)), save=False)
            member.save()

    def _photos(self):
        for i, title in enumerate(PHOTO_TITLES):
            photo = Photo(title=title, author=f"{FIRST[i]} {LAST[i]}", caption=f"{title} — життя компанії «Обрій»")
            photo.image.save(f"seed-{i + 1}.jpg", make_image(i + 120), save=False)
            photo.save()
