# Сервис для хранения скидочных карт "Скидывай" (бэкенд)

### Работающий сервис (до 12/2024) - [skidivay.ru](https://skidivay.ru/)

### Cтэк технологий
- Python 3.11
- Django 4.1
- DjangoRESTframework
- PostgreSQL
- Nginx
- Docker
- Github actions

### Особенности:
- переписана стандартная работа joser и django - после регистрации можно сразу начать пользоваться сервисом, а подтвердить почту позже.
- реализовна работа с рассылкой писем через сервис sendgrid
- работа API полностью покрыта тестами
- CI/CD через Github actions

### Документация
- Правила [разработки](/docs/dev_rules.md) и [кодстайл](/docs/codestyle.md)
- Полная документация по работе с API https://skidivay.ru/api/docs/redoc/ и https://skidivay.ru/api/docs/swagger/

### Разворачиваем проект локально для разработки
1. Клонируйте проект, перейдите в папку `/backend`
2. Убедитесь что poetry установлен. Активируйте виртуальное окружение. Установите зависимости
    ```shell
    poetry shell
    poetry install
    ```
3. Установите pre-commit хуки
    ```shell
    pre-commit install --all
    ```
4. Проведите миграции
    ```shell
    python manage.py migrate
    ```
Файл `.env` для разработки должен находиться в корневой папке проекта.

### Разворачиваем проект локально в контейнерах Docker
   ```shell
   cd ../infra/
   docker-compose up -d --build
   ```
 Файл .env для разворачивания в докере должен находиться в /infra.
