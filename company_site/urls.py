from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("news/", views.news, name="news"),
    path("management/", views.management, name="management"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("contact/", views.contacts, name="contact-alt"),

    # catch-all для кожного розділу; порядок важливий: точні адреси вище,
    # <path:rest> ловить будь-який залишок шляху (разом зі слешами)
    path("news/<path:rest>", views.news, name="news-catchall"),
    path("management/<path:rest>", views.management, name="management-catchall"),
    path("about/<path:rest>", views.about, name="about-catchall"),
    path("contacts/<path:rest>", views.contacts, name="contacts-catchall"),
    path("contact/<path:rest>", views.contacts, name="contact-alt-catchall"),
]
