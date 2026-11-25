from django import template

register = template.Library()


@register.filter
def eur(value) -> str:
    """1500 -> '1 500 €' (кастомний фільтр форматування ціни)."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        return ""
    return f"{number:,}".replace(",", " ") + " €"


@register.filter
def initials(full_name) -> str:
    """'Олена Коваль' -> 'ОК' (для аватара без фото)."""
    return "".join(part[0] for part in str(full_name).split()[:2]).upper()
