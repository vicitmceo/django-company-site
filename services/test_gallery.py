import io
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from PIL import Image

from .models import Photo

TEMP_MEDIA = tempfile.mkdtemp(prefix="test_media_")


def make_image(fmt="PNG", name="photo.png", size=(40, 30)) -> SimpleUploadedFile:
    buffer = io.BytesIO()
    Image.new("RGB", size, (200, 90, 30)).save(buffer, format=fmt)
    return SimpleUploadedFile(name, buffer.getvalue(), content_type=f"image/{fmt.lower()}")


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class GalleryUploadTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def data(self, **extra):
        return {"title": "Команда", "author": "Олена", "caption": "", "image": make_image(), **extra}

    def test_gallery_page_has_multipart_upload_form(self):
        response = self.client.get("/gallery/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, 'type="file"')

    def test_uploaded_photo_is_saved_on_server_disk_and_in_db(self):
        response = self.client.post("/gallery/", self.data(), follow=True)
        photo = Photo.objects.get()
        saved = Path(TEMP_MEDIA) / photo.image.name
        self.assertTrue(saved.is_file(), "файл має лежати в MEDIA_ROOT на сервері")
        self.assertTrue(photo.image.name.startswith("gallery/"))
        self.assertContains(response, "завантажено на сервер")
        self.assertContains(response, photo.image.url)

    def test_non_image_file_is_rejected(self):
        fake = SimpleUploadedFile("evil.txt", b"not an image", content_type="text/plain")
        response = self.client.post("/gallery/", self.data(image=fake))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Photo.objects.count(), 0)

    def test_disguised_file_with_image_extension_is_rejected(self):
        fake = SimpleUploadedFile("evil.png", b"<?php echo 1; ?>", content_type="image/png")
        response = self.client.post("/gallery/", self.data(image=fake))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Photo.objects.count(), 0)

    def test_disallowed_extension_is_rejected(self):
        response = self.client.post("/gallery/", self.data(image=make_image("BMP", "photo.bmp")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Photo.objects.count(), 0)

    def test_too_large_file_is_rejected(self):
        with patch("services.forms.MAX_PHOTO_SIZE", 10):
            response = self.client.post("/gallery/", self.data())
        self.assertContains(response, "завеликий")
        self.assertEqual(Photo.objects.count(), 0)

    def test_missing_fields_show_errors(self):
        response = self.client.post("/gallery/", {})
        self.assertContains(response, "Перевірте, будь ласка")
        self.assertEqual(Photo.objects.count(), 0)
