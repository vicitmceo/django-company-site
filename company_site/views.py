from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from feedback.forms import ContactForm

# Параметр rest потрібен лише для catch-all маршрутів: усе, що йде після
# базової адреси розділу (наприклад /news/2026), ігнорується, і показується
# головна сторінка цього розділу.


HIGHLIGHTS = [
    ("web", "Веб-розробка", "icon-web.svg", "Сайти, магазини та вебсервіси під ключ."),
    ("mobile", "Мобільні застосунки", "icon-mobile.svg", "Додатки для iOS та Android."),
    ("ai", "ШІ та автоматизація", "icon-ai.svg", "Чат-боти та аналітика даних."),
    ("support", "Підтримка", "icon-support.svg", "Стабільність ваших продуктів 24/7."),
]


def home(request):
    return render(request, "home.html", {"highlights": HIGHLIGHTS})


def news(request, rest=None):
    return render(request, "news.html", {"active": "news"})


def management(request, rest=None):
    return render(request, "management.html", {"active": "management"})


def about(request, rest=None):
    return render(request, "about.html", {"active": "about"})


def contacts(request, rest=None):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Дякуємо! Ваше повідомлення надіслано, ми відповімо найближчим часом.")
            # Post/Redirect/Get: оновлення сторінки не відправить форму вдруге
            return redirect(f"{request.path}#contact-form")
    else:
        form = ContactForm()
    return render(request, "contacts.html", {"active": "contacts", "form": form})


# Підрозділи існуючих розділів: розділ -> {slug: дані сторінки}
SUBSECTIONS = {
    "contacts": {
        "france": {
            "title": "Офіс у Франції",
            "lines": ["м. Париж, Rue de Rivoli, 12", "+33 1 23 45 67 89", "paris@obriy.example"],
        },
        "ukraine": {
            "title": "Офіс в Україні",
            "lines": ["м. Київ, вул. Хрещатик, 1, офіс 25", "+380 44 123 45 67", "kyiv@obriy.example"],
        },
        "austria": {
            "title": "Офіс в Австрії",
            "lines": ["м. Відень, Ringstrasse, 8", "+43 1 234 56 78", "vienna@obriy.example"],
        },
    },
    "about": {
        "history": {
            "title": "Наша історія",
            "lines": ["2016 — заснування компанії командою з трьох людей.",
                      "2020 — відкриття першого закордонного офісу.",
                      "2026 — понад 80 фахівців і 200 завершених проєктів."],
        },
        "mission": {
            "title": "Місія та цінності",
            "lines": ["Робити технології зрозумілими та корисними для бізнесу.",
                      "Чесність, якість, повага до клієнтів, постійне навчання."],
        },
    },
    "management": {
        "director": {
            "title": "Генеральний директор",
            "lines": ["Олександр Коваленко",
                      "Керує стратегією компанії та ключовими партнерствами."],
        },
        "cto": {
            "title": "Технічний директор",
            "lines": ["Марія Шевчук",
                      "Відповідає за архітектуру продуктів та технічну команду."],
        },
    },
}

SECTION_TITLES = {"contacts": "Контакти", "about": "Про компанію", "management": "Керівництво"}


def subsection(request, section, slug):
    page = SUBSECTIONS.get(section, {}).get(slug)
    if page is None:
        raise Http404("Підрозділ не знайдено")
    context = {
        "active": section,
        "page": page,
        "section": section,
        "section_title": SECTION_TITLES[section],
        "siblings": [(key, value["title"]) for key, value in SUBSECTIONS[section].items()],
    }
    return render(request, "subsection.html", context)


def not_found(request, exception=None, rest=None):
    """Сторінка 404 для неіснуючих розділів (працює і як handler404)."""
    return render(request, "404.html", status=404)
