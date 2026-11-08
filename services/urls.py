from django.urls import path, re_path

from . import views

app_name = "services"

# Підрозділи: /services/web, /services/mobile, /services/ai, /services/support
# (слеш наприкінці необов'язковий); усе інше під /services/ веде на список послуг.
urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^(?P<slug>web|mobile|ai|support)/?$", views.detail, name="detail"),
    path("<path:rest>", views.index, name="catchall"),
]
