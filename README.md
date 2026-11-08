# Вебдодаток «Інформація про компанію» (Django)

Багатороздільний сайт компанії на Django без форм, моделей і БД: лише маршрутизація, views та шаблони.

| Розділ | Адреса |
|--------|--------|
| Головна | `/` |
| Новини | `/news/` |
| Керівництво | `/management/` |
| Про компанію | `/about/` |
| Контакти | `/contacts/` або `/contact/` |

Будь-який додатковий шлях після адреси розділу (`/news/2026`, `/about/team/2020`,
`/contacts/odesa/tairovo`) показує головну сторінку цього розділу (catch-all `<path:rest>`).

## Структура
```
company_site_proj/
├── manage.py
├── company_site/   (settings.py, urls.py, views.py, tests.py)
├── templates/      (base.html, home.html, news.html, management.html, about.html, contacts.html)
└── requirements.txt
```

## Запуск
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```
Відкрити: http://127.0.0.1:8000

Тести: `python manage.py test`
