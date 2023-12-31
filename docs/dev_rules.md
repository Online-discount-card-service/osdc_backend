## Что сделано и чем отличается от структуры по умолчанию
- poetry как менеджер пакетов и управления зависимостями
- базовые линтеры (black, flake8)
- pre-commit хуки
- используется PostgreSQL, если параметры не прописаны в .env, то SQLite
- автодокументация swagger/redoc (http://base_url/api/v1/docs/swagger-ui/ или http://base_url/api/v1/docs/redoc/)

## Общие требования к стилю кода - [ссылка](codestyle.md)

## Правила работы с git (как делать коммиты и pull request-ы)
1. Две основные ветки: `main` и `develop`. CI/CD настроен так, что при пуше в любую происходит деплой на сервер.
2. В `main` находится только production-ready код. PR из develop раз в неделю через ревью ментора.
3. Ветка `develop` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код. Сливаем в нее свои ветки через PR с как минимум одним аппрувом.
4. Создавая новую ветку, наследуйтесь от ветки `develop`
5. Правила именования веток
    - весь новый функционал — `feature/название-функционала`
    - исправление ошибок — `fix/название-багфикса`
6. PR в `develop` и `master` должны быть базово покрыты тестами:
    - на доступность эндпойнтов
    - проверка списка полей
    - проверен критичный функционал (пример: фильтр по слову “сосиска” возвращает только результаты с “сосиска“)

## Подготовка окружения для разработки

### Предварительные требования:
1. **Poetry** \
Зависимости и пакеты управляются через **poetry**. Убедитесь, что **poetry** [установлен](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) на вашем компьютере и ознакомьтесь с [документацией](https://python-poetry.org/docs/cli/).
2. **Docker** \
В проекте используется PostgreSQL. Рекомендуем запускать БД через Docker, следуя [инструкциям](../README.md).
3. Файлы **requirements** \
Файлы редактировать вручную не нужно. Обновляются через pre-commit хуки (если есть изменение в зависимостях, то список обновится при коммите).
4. **pre-commit хуки** \
[Документация](https://pre-commit.com)\
При каждом коммите выполняются хуки (автоматизации) перечисленные в **.pre-commit-config.yaml**. Если не понятно какая ошибка мешает сделать коммит можно запустить хуки вручную и посмотреть ошибки:
    ```shell
    pre-commit run --all-files
    ```
