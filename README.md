# Вебдодаток «Інформація про компанію» (Django)

Багатороздільний сайт компанії «Обрій» на Django без форм, моделей і БД: лише маршрутизація, views, шаблони та статика (CSS, SVG-зображення).

| Розділ | Адреса |
|--------|--------|
| Головна | `/` |
| Новини | `/news/` |
| Керівництво | `/management/` |
| Про компанію | `/about/` |
| Контакти | `/contacts/` або `/contact/` |
| Послуги (окремий додаток `services`) | `/services/` |

## Підрозділи
- Контакти: `/contacts/france`, `/contacts/ukraine`, `/contacts/austria`
- Послуги: `/services/web`, `/services/mobile`, `/services/ai`, `/services/support`
- Про компанію: `/about/history`, `/about/mission`
- Керівництво: `/management/director`, `/management/cto`

## Неіснуючі адреси
Усе, що не належить жодному розділу (`/blog/`, `/xyz`), показує сторінку **404** (`templates/404.html`).
Неіснуючі підшляхи *всередині* розділу показують головну сторінку цього розділу.

Будь-який додатковий шлях після адреси розділу (`/news/2026`, `/about/team/2020`,
`/contacts/odesa/tairovo`) показує головну сторінку цього розділу (catch-all `<path:rest>`).

## Структура
```
company_site_proj/
├── manage.py
├── company_site/   основний додаток (settings.py, urls.py, views.py, tests.py)
├── services/       другий додаток: розділ «Послуги» та його підрозділи
├── static/         css/style.css, img/*.svg
├── templates/      base.html, home.html, news.html, management.html, about.html,
│                   contacts.html, subsection.html, 404.html, services/
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
