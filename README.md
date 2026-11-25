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
| Галерея з формою завантаження фото | `/gallery/` |
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
├── media/          завантажені файли (зображення з БД та фото з форми галереї)
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
python manage.py seed        # демо-дані: по 22–25 рядків у кожній таблиці + зображення в media/
python manage.py runserver
```
Відкрити: http://127.0.0.1:8000

Тести: `python manage.py test`

## Форма контактів
На `/contacts/` (і `/contact/`) є форма: ім'я, email, телефон (необов'язково), тема, повідомлення (мін. 20 символів).
Дані валідуються на сервері, зберігаються в `ContactMessage` і доступні в адмінці Django (`/admin/`, потрібен `createsuperuser`).

## Моделі (`services/models.py`, 5 моделей по 5–6 полів)
`Service` (послуги), `Project` (проєкти, FK на послугу), `NewsArticle` (новини), `TeamMember` (керівництво/команда), `Photo` (фото галереї).
Міграція: `services/migrations/0001_initial.py`. Усі моделі зареєстровані в адмінці (`/admin/`).

## Медіа та завантаження фото
`MEDIA_ROOT = media/`, `MEDIA_URL = /media/` (у DEBUG роздається Django). Зображення моделей лежать у `media/services|projects|news|team/`.
Сторінка `/gallery/` містить форму завантаження фото (`multipart/form-data`): файл перевіряється (тип, розширення jpg/png/webp/gif, до 5 МБ)
і зберігається на сервері в `media/gallery/`, а запис — у БД.

## Шаблони
`base.html` з наслідуванням, теги `with`, `if/else`, `for`, стандартні фільтри (`length`, `date`, `truncatewords`) та власні фільтри
`eur`, `initials` (`services/templatetags/company_filters.py`). Views передають складні словники з колекціями власних класів
`Stat`, `SectionLink` (`company_site/blocks.py`).
