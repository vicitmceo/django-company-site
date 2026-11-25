"""Власні класи, які views передають у шаблони в складних словниках контексту."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Stat:
    """Число з підписом для блоку «Компанія в цифрах»."""

    value: str
    label: str


@dataclass(frozen=True)
class SectionLink:
    """Посилання-картка на розділ сайту."""

    title: str
    text: str
    url_name: str
