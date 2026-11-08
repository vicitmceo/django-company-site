from django.urls import include, path, re_path

from . import views

# Підрозділи (/contacts/france, /about/history, ...): адреси з опціональним слешем.
# Мають стояти ВИЩЕ за catch-all, інакше /contacts/france покаже головну контактів.
subsection_routes = [
    re_path(
        rf"^{section}/{slug}/?$",
        views.subsection,
        {"section": section, "slug": slug},
        name=f"{section}-{slug}",
    )
    for section, pages in views.SUBSECTIONS.items()
    for slug in pages
]

handler404 = "company_site.views.not_found"

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", include("services.urls")),  # окремий додаток
    path("news/", views.news, name="news"),
    path("management/", views.management, name="management"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("contact/", views.contacts, name="contact-alt"),

    *subsection_routes,

    # catch-all для кожного розділу; порядок важливий: точні адреси вище,
    # <path:rest> ловить будь-який залишок шляху (разом зі слешами)
    path("news/<path:rest>", views.news, name="news-catchall"),
    path("management/<path:rest>", views.management, name="management-catchall"),
    path("about/<path:rest>", views.about, name="about-catchall"),
    path("contacts/<path:rest>", views.contacts, name="contacts-catchall"),
    path("contact/<path:rest>", views.contacts, name="contact-alt-catchall"),

    # будь-який інший (неіснуючий) розділ -> сторінка 404
    re_path(r"^.*$", views.not_found, name="not-found"),
]
