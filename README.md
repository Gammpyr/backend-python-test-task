# Backend Python Test Task
## Требования
- Python 3.12
- Poetry
- PostgreSQL

## Установка и запуск
1) Клонировать репозиторий

2) Установить зависимости:
```bash
poetry install
```
3) Создать файл .env на основе .env.example и заполнить параметры подключения к БД

4) Выполнить миграции:
```bash
poetry run python manage.py migrate
```

5) Создать суперпользователя:
```bash
poetry run python manage.py createsuperuser
```

6) Запустить сервер:
```bash
poetry run python manage.py runserver
```
## API Endpoints
Категории и продукты (доступ без авторизации)
```
GET /category/ - список категорий (пагинация 5 записей)

GET /product/ - список продуктов (пагинация 5 записей)
```
Аутентификация (JWT)
```
POST /users/api/token/ - получение access/refresh токенов

POST /users/api/token/refresh/ - обновление access токена
```
Корзина (Только для авторизованных пользователей)
```
POST /update-cart-item/ - добавление/изменение количества товара

GET /get-cart-items-list/ - просмотр корзины

POST /clear_cart/ - очистка корзины
```
### Админка

- Адрес: /admin/
- Управление категориями 
- Управление продуктами 

### Документация
```
Swagger UI: /swagger/

ReDoc: /redoc/
```
# Тестовое задание 1

Запуск программы:

```bash
poetry run python main.py
```
Введите число и программа выведет последовательность вида: 122333444455555...