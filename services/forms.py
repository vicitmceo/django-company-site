from django import forms
from django.core.validators import FileExtensionValidator

from .models import Photo

MAX_PHOTO_SIZE = 5 * 1024 * 1024  # 5 МБ
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "gif"]


class PhotoForm(forms.ModelForm):
    """Форма завантаження фото: файл потрапляє на сервер у MEDIA_ROOT/gallery/."""

    image = forms.ImageField(
        label="Фото",
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS)],
        help_text="JPG, PNG, WEBP або GIF, до 5 МБ.",
        widget=forms.ClearableFileInput(attrs={"accept": "image/*"}),
    )

    class Meta:
        model = Photo
        fields = ["title", "author", "caption", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Наприклад: Команда на корпоративі"}),
            "author": forms.TextInput(attrs={"placeholder": "Ваше ім'я", "autocomplete": "name"}),
            "caption": forms.TextInput(attrs={"placeholder": "Короткий підпис (необов'язково)"}),
        }

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image.size > MAX_PHOTO_SIZE:
            raise forms.ValidationError("Файл завеликий: максимум 5 МБ.")
        return image
