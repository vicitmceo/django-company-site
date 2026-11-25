from django.db import models


class ContactMessage(models.Model):
    name = models.CharField("Ім'я", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=30, blank=True)
    subject = models.CharField("Тема", max_length=150)
    message = models.TextField("Повідомлення")
    created_at = models.DateTimeField("Надіслано", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "повідомлення з форми контактів"
        verbose_name_plural = "повідомлення з форми контактів"

    def __str__(self) -> str:
        return f"{self.name}: {self.subject}"
