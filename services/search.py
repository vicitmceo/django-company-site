from dataclasses import dataclass

from .models import NewsArticle, Project, Service

MIN_QUERY_LENGTH = 2
MAX_PER_GROUP = 12


@dataclass(frozen=True)
class SearchResults:
    """Результати пошуку, згруповані за типом."""

    query: str
    services: list
    news: list
    projects: list

    @property
    def total(self) -> int:
        return len(self.services) + len(self.news) + len(self.projects)


def _matches(needle: str, *values: str) -> bool:
    # casefold у Python: SQLite icontains не ігнорує регістр для кирилиці
    return any(needle in value.casefold() for value in values)


def search_site(query: str) -> SearchResults:
    query = query.strip()
    needle = query.casefold()
    if len(needle) < MIN_QUERY_LENGTH:
        return SearchResults(query, [], [], [])

    services = [s for s in Service.objects.all() if _matches(needle, s.title, s.summary)]
    news = [n for n in NewsArticle.objects.all() if _matches(needle, n.title, n.summary, n.category)]
    projects = [
        p for p in Project.objects.select_related("service")
        if _matches(needle, p.title, p.client, p.service.title)
    ]
    return SearchResults(query, services[:MAX_PER_GROUP], news[:MAX_PER_GROUP], projects[:MAX_PER_GROUP])
