from django.db import models


class Service(models.Model):
    title = models.CharField("Назва", max_length=120)
    slug = models.SlugField("Адреса (slug)", unique=True)
    summary = models.CharField("Короткий опис", max_length=255)
    points = models.TextField("Що входить (по рядку)", help_text="Кожен пункт з нового рядка")
    price_from = models.PositiveIntegerField("Ціна від, €")
    image = models.ImageField("Зображення", upload_to="services/")

    class Meta:
        ordering = ["id"]
        verbose_name = "послуга"
        verbose_name_plural = "послуги"

    def __str__(self) -> str:
        return self.title

    @property
    def point_list(self) -> list[str]:
        return [line.strip() for line in self.points.splitlines() if line.strip()]


class Project(models.Model):
    title = models.CharField("Назва", max_length=150)
    client = models.CharField("Клієнт", max_length=120)
    year = models.PositiveSmallIntegerField("Рік")
    description = models.TextField("Опис")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="projects", verbose_name="Послуга")
    image = models.ImageField("Зображення", upload_to="projects/")

    class Meta:
        ordering = ["-year", "-id"]
        verbose_name = "проєкт"
        verbose_name_plural = "проєкти"

    def __str__(self) -> str:
        return self.title


class NewsArticle(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    category = models.CharField("Категорія", max_length=40)
    summary = models.CharField("Анонс", max_length=300)
    body = models.TextField("Текст")
    published_at = models.DateField("Дата публікації")
    image = models.ImageField("Зображення", upload_to="news/")

    class Meta:
        ordering = ["-published_at", "-id"]
        verbose_name = "новина"
        verbose_name_plural = "новини"

    def __str__(self) -> str:
        return self.title


class TeamMember(models.Model):
    full_name = models.CharField("Ім'я та прізвище", max_length=120)
    position = models.CharField("Посада", max_length=120)
    department = models.CharField("Відділ", max_length=80)
    bio = models.TextField("Про себе")
    email = models.EmailField("Email")
    photo = models.ImageField("Фото", upload_to="team/")

    class Meta:
        ordering = ["id"]
        verbose_name = "співробітник"
        verbose_name_plural = "співробітники"

    def __str__(self) -> str:
        return self.full_name


class Photo(models.Model):
    """Фото, завантажене відвідувачем через форму; файл зберігається в MEDIA_ROOT/gallery/."""

    title = models.CharField("Назва", max_length=100)
    author = models.CharField("Автор", max_length=80)
    caption = models.CharField("Підпис", max_length=255, blank=True)
    image = models.ImageField("Фото", upload_to="gallery/")
    uploaded_at = models.DateTimeField("Завантажено", auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at", "-id"]
        verbose_name = "фото"
        verbose_name_plural = "фото галереї"

    def __str__(self) -> str:
        return self.title
