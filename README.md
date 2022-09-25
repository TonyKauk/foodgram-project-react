# Foodgram Project
## Описание
Проект **Foodgram** позволяет пользователям создавать и хранить рецепты,
подписываться на авторов рецептов, добавлять рецепты в корзину и выгружать их
в виде списка игредиентов с их просуммированным количеством.

## Технологии
- Проект написан на Python 3.8.9
- Фрэймворк Django 4.1.1
- Использовался Django Framework 3.13.1
- Применен модуль Djoser 2.1.0
- Для работы с изображениями использовался Pillow 9.2.0

## Запуск проекта

Клонировать репозиторий и перейти в него в командной строке:
```git clone <ссылка>```
```сd <папка проекта>```
Запустите Docker и в папке infra выполните:
```docker-compose up```
Теперь по адресу **http://localhost/api/docs/** доступно подробное описание функционала проекта в Redoc

Cоздать и активировать виртуальное окружение:
```python3 -m venv env```
```source env/bin/activate```
Установить установщик пакетов:
```python3 -m pip install --upgrade pip```
Установить зависимости из файла requirements.txt:
```pip install -r requirements.txt```
Установить flake8 с необходимыми модулями:
```pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort```
Выполнить миграции:
```python3 manage.py migrate```
Запустить проект:
```python3 manage.py runserver```


Установка npm:
**https://nodejs.org/en/download/**
Запуск фронтэнда:
```npm i```
```npm run start```

## Автор
Антон Милов
