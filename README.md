# GlobalCRM

GlobalCRM разрабатывается для оптимизации рабочих процессов сотрудников в малых организациях, предоставляя инструменты для эффективного управления задачами и уведомлений о новых поручениях или приближающихся сроках выполнения. <p> Система позволяет руководителям управлять задачами, а сотрудникам получать уведомления о новых задачах, управлять своими поручениями и загружать документы в процессе выполнения задачи. Каждая задача может иметь несколько этапов выполнения, предоставляя подробную историю ее прогресса.
<p>CRM-система направлена на улучшение коммуникации и управления задачами в организации, предоставляя интуитивно понятный интерфейс как для руководителей, так и для сотрудников<p>

*Данная документация и функции постепенно пополняются в процессе разработки.*

## Технологии
- Python 3.11.5
- Django 4.2.7
- PostgresSQL
- Docker

## Основные возможности

- **Управление задачами:**
  - Создание, редактирование и удаление задач.
  - Назначение задач конкретным сотрудникам.
  - Категоризация задач для быстрого создания (например, юридические, жалобы, регистрация).

- **Управление документами:**
  - Загрузка и предварительный просмотр документов, связанных с каждой задачей.
  - Просмотр всех документов, связанных с конкретной задачей.

- **Эффективность рабочего процесса:**
  - Добавление и управление этапами выполнения задачи.
  - Получение уведомлений о приближающихся сроках.

- **Профиль:**
  - Профили сотрудников содержат календарь для отслеживания текущих задач.



*(В просессе написания...) <p>*

## Запуск проекта для целей разработки

1. Склонируйте репозиторий:

    ```
    git clone https://github.com/eltimccc/globalcrm.git
    ```
2. Создайте виртуальное окружение и активируйте его:
    ```
    python3 -m venv venv
    source venv/bin/activate  # для Unix/Mac
    ```
3. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
4. Примените миграции:
    ```
    python manage.py migrate
    ```
5. Запустите сервер разработки:
    ```
    python manage.py runserver    
    ```

### Запуск в Docker

1. Склонируйте репозиторий:

    ```
    git clone 
    ```

2. Из папки проекта запустите контейнер:
    ```
    docker-compose up -d --build
    ```

3. Создайте суперпользователя:
    ```
    docker-compose run web python manage.py createsuperuser
    ```

4. После удачной сборки и запуска контейнера приложение будет доступно на http://localhost:8000.


### Автор
[Денис М. (Python-разработчик)](https://github.com/eltimccc "Денис М. (Python-разработчик)")