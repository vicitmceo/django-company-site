from django.shortcuts import render

SERVICES = {
    "web": {
        "title": "Веб-розробка",
        "icon": "icon-web.svg",
        "summary": "Сайти, інтернет-магазини та вебсервіси під ключ.",
        "points": ["Корпоративні сайти та лендінги", "Інтернет-магазини з оплатою онлайн",
                   "Адмін-панелі та особисті кабінети", "Адаптивна верстка під будь-який екран"],
        "price": "від 1 500 €",
    },
    "mobile": {
        "title": "Мобільні застосунки",
        "icon": "icon-mobile.svg",
        "summary": "Додатки для iOS та Android: від прототипу до магазину застосунків.",
        "points": ["Нативні та кросплатформні рішення", "Push-сповіщення та офлайн-режим",
                   "Інтеграція з вашим сервером", "Публікація в App Store та Google Play"],
        "price": "від 3 000 €",
    },
    "ai": {
        "title": "ШІ та автоматизація",
        "icon": "icon-ai.svg",
        "summary": "Чат-боти, аналітика даних і автоматизація рутинних процесів.",
        "points": ["Чат-боти для клієнтської підтримки", "Автоматична обробка документів",
                   "Прогнозування та аналітика", "Інтеграція мовних моделей у ваші продукти"],
        "price": "від 2 000 €",
    },
    "support": {
        "title": "Підтримка та супровід",
        "icon": "icon-support.svg",
        "summary": "Стежимо за стабільністю ваших продуктів, поки ви ведете бізнес.",
        "points": ["Моніторинг та швидке реагування", "Регулярні оновлення та резервні копії",
                   "Технічні консультації", "Договір із гарантованим часом відповіді"],
        "price": "від 300 € / міс.",
    },
}


def index(request, rest=None):
    context = {"active": "services", "services": SERVICES.items()}
    return render(request, "services/index.html", context)


def detail(request, slug):
    context = {
        "active": "services",
        "slug": slug,
        "service": SERVICES[slug],
        "others": [(key, value["title"]) for key, value in SERVICES.items() if key != slug],
    }
    return render(request, "services/detail.html", context)
