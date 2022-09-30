# api yamdb

## Что это за проект?

> Это API для проекта Yamdb, позволяющая получать, удалять, редактировать
> данные о произведениях и пользователях
> Все данные возвращаются в формате JSON 

## Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Serenityblood/api_yamdb.git
cd api_yamdb
```

### Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

### Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### Выполнить миграции:

```
python3 manage.py migrate
```

### Запустить проект:

```
python3 manage.py runserver
```

## Документация:
> Находится на эндпоинте: http://127.0.0.1:8000/redoc/ с примерами ответов API
