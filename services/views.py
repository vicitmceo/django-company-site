from django.shortcuts import render

from .models import Service


def index(request, rest=None):
    return render(request, "services/index.html", {"active": "services", "services": Service.objects.all()})


def detail(request, slug):
    service = Service.objects.filter(slug=slug).first()
    if service is None:  # неіснуючий підрозділ -> список послуг
        return index(request)
    context = {
        "active": "services",
        "service": service,
        "others": Service.objects.exclude(pk=service.pk)[:8],
        "projects": service.projects.all()[:3],
    }
    return render(request, "services/detail.html", context)
