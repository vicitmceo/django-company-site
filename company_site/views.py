from django.shortcuts import render

# Параметр rest потрібен лише для catch-all маршрутів: усе, що йде після
# базової адреси розділу (наприклад /news/2026), ігнорується, і показується
# головна сторінка цього розділу.


def home(request):
    return render(request, "home.html")


def news(request, rest=None):
    return render(request, "news.html", {"active": "news"})


def management(request, rest=None):
    return render(request, "management.html", {"active": "management"})


def about(request, rest=None):
    return render(request, "about.html", {"active": "about"})


def contacts(request, rest=None):
    return render(request, "contacts.html", {"active": "contacts"})
