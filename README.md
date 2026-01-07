# **Проект интернет магазина**
## Описание:
На данном этапе есть приложение catalog с домашней страницей и контактной информацией с обратной связью

## Установка:
1. Клонируйте репозиторий:
```https://github.com/AntonSmolyaninov/HomeWorkDjango```
2. Установите зависимости:
- `poetry init` — инициализировать пакет в существующем проекте.
- `poetry new package-name` — создать новый проект.
- `poetry install (dependency name)` — первичная установка.
- `poetry update` — обновление зависимостей.
- `poetry remove (dependency name)` — удалить зависимость из проекта.
- `poetry show--tree` — посмотреть всё дерево зависимостей.
- `poetry show --latest`— посмотреть, последние ли версии используются в проекте.
- `poetry add django` - установка Django
- `django-admin startproject config .` - создание django проекта c настройками в директории config
- `python manage.py startapp "name app"` - создание приложения
## Запуск
`poetry run python manage.py runserver`

