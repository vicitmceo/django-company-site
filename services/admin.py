from django.contrib import admin

from .models import NewsArticle, Photo, Project, Service, TeamMember


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "price_from")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "year", "service")
    list_filter = ("year", "service")
    search_fields = ("title", "client")


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at")
    list_filter = ("category",)
    search_fields = ("title", "summary")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "department", "email")
    list_filter = ("department",)
    search_fields = ("full_name", "position")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "uploaded_at")
    search_fields = ("title", "author", "caption")
    readonly_fields = ("uploaded_at",)
