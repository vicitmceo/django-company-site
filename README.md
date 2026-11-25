# Вебдодаток «Інформація про компанію» (Django)

Багатороздільний сайт компанії «Обрій» на Django: маршрутизація, views, шаблони, статика (CSS, SVG-зображення) та форма зворотного зв'язку з БД (SQLite).

| Розділ | Адреса |
|--------|--------|
| Головна | `/` |
| Новини | `/news/` |
| Керівництво | `/management/` |
| Про компанію | `/about/` |
| Контакти | `/contacts/` або `/contact/` |
| Послуги (окремий додаток `services`) | `/services/` |
| Форма зворотного зв'язку (додаток `feedback`) | на сторінці `/contacts/` |

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
├── feedback/       форма контактів: модель ContactMessage, форма з валідацією, адмінка
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
python manage.py migrate
python manage.py runserver
```
Відкрити: http://127.0.0.1:8000

Тести: `python manage.py test`

## Форма контактів
На `/contacts/` (і `/contact/`) є форма: ім'я, email, телефон (необов'язково), тема, повідомлення (мін. 20 символів).
Дані валідуються на сервері, зберігаються в `ContactMessage` і доступні в адмінці Django (`/admin/`, потрібен `createsuperuser`).
