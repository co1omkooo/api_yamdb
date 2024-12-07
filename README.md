# api_yamdb
API для сервиса yamdb. Позволяет оценить произведение и оставить отзыв о нём.

## Как запустить
1. Клонируем репозиторий и переходим в него в командной строке

```
git clone https://github.com/co1omkooo/api_yamdb/
```

```
cd api_yamdb
```

2. Создаем и активируем виртуальное окружение

```
python -m venv venv
```

```
source venv/Scripts/activate
```

3. Устанавливаем необходимые зависимости из requirements

```
pip install -r requirements.txt
```

4. Делаем миграции

```
python api_yamdb/manage.py migrate
```

5. Запускаем проект

```
python api_yamdb/manage.py runserver
```

### Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям, может отсавлять коментарии; может редактировать и удалять свои отзывы и комментарии.
- Модератор (moderator) — те же права, что и у пользователя, так же права удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта.
- Суперюзер Django — обладает правами администратора (admin)

### Примеры работы с API для всех пользователей

Подробная документация доступна по эндпоинту /redoc/

Для неавторизованных пользователей работа с API доступна в режиме чтения, что-либо изменить или создать не получится. 

```
Права доступа: Доступно без токена.
GET /api/v1/categories/ - Получение списка всех категорий
GET /api/v1/genres/ - Получение списка всех жанров
GET /api/v1/titles/ - Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ - Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Получение списка всех комментариев к отзыву
Права доступа: Администратор
GET /api/v1/users/ - Получение списка всех пользователей
```

### Регистрация нового пользователя
Регистрация нового пользователя:
Права доступа: Доступно без токена.
```
POST /api/v1/auth/signup/
```

```json
{
  "email": "string",
  "username": "string"
}

```

Получение JWT-токена:

```
POST /api/v1/auth/token/
```

```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

### Примеры работы с API для авторизованных пользователей

Добавление категории:

```
Права доступа: Администратор.
POST /api/v1/categories/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление категории:

```
Права доступа: Администратор.
DELETE /api/v1/categories/{slug}/
```

Добавление жанра:

```
Права доступа: Администратор.
POST /api/v1/genres/
```

```json
{
  "name": "string",
  "slug": "string"
}
```

Удаление жанра:

```
Права доступа: Администратор.
DELETE /api/v1/genres/{slug}/
```

Обновление публикации:

```
PUT /api/v1/posts/{id}/
```

```json
{
"text": "string",
"image": "string",
"group": 0
}
```

Добавление произведения:

```
POST /api/v1/titles/
```

```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}

### Работа с пользователями:

Для работы с пользователя есть некоторые ограничения для работы с ними.
Получение списка всех пользователей.

```
GET /api/v1/users/ - Получение списка всех пользователей
```

Добавление пользователя:

```
Поля email и username должны быть уникальными.
POST /api/v1/users/ - Добавление пользователя
```

```json
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```

Получение пользователя по username:

```
GET /api/v1/users/{username}/ - Получение пользователя по username
```

Изменение данных пользователя по username:

```
PATCH /api/v1/users/{username}/ - Изменение данных пользователя по username
```

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```