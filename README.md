# Проект Blogicum

## Цель работы:

Научится следующему:  
1. Подключать к проекту кастомные страницы для ошибок. :heavy_check_mark:
2. Работать с моделью пользователя в проекте. :heavy_check_mark: :grey_question:
3. Подключать пагинацию к страницам. :heavy_check_mark:
4. Работать с изображениями. :heavy_check_mark: :grey_question:
5. Работать с *view-классами*. :heavy_check_mark:
6. Создавать права доступа для пользователей. :heavy_check_mark:

## Разворачивание проекта.

1. Установить виртуальное окружение.

```bash
python -m venv venv
```

2. Активировать виртуальное окружение.

```bash
. venv/Scripts/activate
```

3. Установить зависиости из requirements.txt.

```bash
pip install -r requirements.txt
```

4. Перейти в директорию с файлом "manage.py".

```bash
cd ./<название_директории>/
```

5. Применить миграции.

```bash
python manage.py migrate
```

6. Создать суперпользователя.

```bash
python manage.py createsuperuser
```

7. Запустить сервер.

```bash
python manage.py runserver
```

8. Наслаждаться :coffee:  

**Приведенные команды используются для Bash/OC Windows*  
**Это третий спринт из курса "Бэкенд на Django Ver.2.0" от Яндекс.Практикум*
