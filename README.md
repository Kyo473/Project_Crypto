<h1 align="center">FastexChange</h1>
<p>
Платформа для обмена криптовалюты

Описание: Cервис позволит жителям одного региона обмениваться криптовалютой между собой, используя гео-данные для нахождения ближайших сделок и контроля над безопасностью обмена.
<p>

## Информация
- Title:  `FastexChange`
- Authors:  `Denis Kepich`

<h3>Ссылки:</h3>

- [FastexChange](#FastexChange)
    - [Services](#services)
    - [API](##API)
    - [Deploy](#Deploy)
    - [Tests](Services/ChatService/README.md)
    - [Notifications](Services/NotifyService/README.md)
    - [Roadmap ](#Roadmap)
- [Readme]
    - [UserService](Services/UserService/README.md)
    - [PolicyService](Services/PolicyService/README.md)
    - [TradeService](Services/TradeService/README.md)
    - [ChatService](Services/ChatService/README.md)
    - [NotifyService](Services/NotifyService/README.md)

# Deploy
## Установка и зависимости
Каждый микросервис имеет файл requirements.txt, который содержит все зависмости для работы микросервисов

## После сборки проекта доступен:
- e2e тест в Docker
  ```
  deploy-test-runner-1
  ```
- Unit тест в сервисе чата
  ```bash
  python -m unittest
  ```

## Services

1. Сервис управления пользователями(UserService):

 - Отвечает за регистрацию и аутентификацию пользователя.
 - Хранит информацию о пользователе в базе данных PostgreSQL.

2. Сервис управления доступом(PolicyService):

 - Отвечает за управление правами доступа пользователя
 - Обеспечивает генерацию и проверку токенов доступа для авторизации пользователя.

3. Сервис управления сделками(TradeService):

 - Отвечает за добавление, редактирование и удаление сделок.
 - Хранит информацию о сделках в базе данных PostgreSQL.

4. Сервис управления чатами(ChatService):

 - Отвечает за создание вебсоект соединения и хранение сообщений.
 - Хранит информацию о сообщениях в базе данных PostgreSQL.

5. Сервис управления уведомлениями (NotifyService):

 - Отвечает за отправление сообщений при регистрации пользователя

## API

1. UserService:
    - `POST` **/auth/register** - создание нового пользователя 
    - `POST` **/auth/jwt/login** - Авторизация пользователя
    - `POST` **/auth/jwt/logout** - Выход пользователя из системы
    - `GET` **/users/me** - Получение информации о себе
    - `GET` **/users/{id}** - Получение информации о другом пользователе
    - `PATCH` **/users/me** - Обновление информации о себе
    - `PATCH` **/users/{id}** - Обновление информации о другом пользователе
    - `DELETE` **users/{id}** - Удаление пользователя 
2. PolicyService:
    - Не имеет API
3. TradeService:
     - `POST` **/trade** - создание новой сделки
     - `GET` **/trades**  - Получение всех сделок
     - `GET` **/trades/{TradeId}** - Получение конкретной сделки
     - `PATCH` **/trades/{TradeId}** - Обновление конкретной сделки
     - `PATCH` **/trades/{TradeId}/accept** - Принять сделку
     - `PUT` **/trades/{TradeId}** - Обновляет информацию сделки для админа
     - `DELETE` **/trades/{TradeId}** - Удаление сделки
     - `GET` **/point_in_range/** - Возвращает информацию о сдлках в радиусе
     - `GET` **/nearest** - Поиск ближайщей сделки
     - `GET` **/visualize** - Отображение сделок на карте (Требуется при отсутствии фронта)
4. ChatService:
     - `POST` **/chatroom** - создание нового чата 
     - `GET` **/chatroom/{RoomID}**  - Возвращает информацию о чате
     - `GET` **/chat**  - Открывает html с чатом пользователей (Требуется при отсутствии фронта)
     - `WS` **/ws/{RoomID}/{client_id}**  - Эндпоинт для подключения к чату
     - `GET` **/last_messages/{RoomID}**  - Получение прошлых сообщений в чате и БД по её RoomID

5. NotifyService:
     - Не имеет API
# Frontend
Был создан макет для тестирования регистрации и веб-сокет соединений.Приложение не является MVP.
Доступен после сборки http://localhost:3000
# Roadmap 
  - Написать Frontend для приложения 
  - Написать Смарт-контракт для крипто-платежей
  - Реализовать сервис проверки транзакций 
  - Добавить метрики курсов криптовалют
## Иерархия каталогов
```
|—— .gitignore
|—— deploy
|    |—— .env
|    |—— docker-compose.yml
|    |—— e2e
|        |—— test.py
|    |—— policy-enforcement-service
|        |—— policies.yaml
|—— Services
|    |—— ChatService
|        |—— .dockerignore
|        |—— .env
|        |—— app
|            |—— app.py
|            |—— chat
|                |—— crud.py
|                |—— database.py
|                |—— models.py
|                |—— schemas.py
|                |—— __init__.py
|            |—— config.py
|            |—— templates
|                |—— chat.html
|            |—— __init__.py
|        |—— Dockerfile
|        |—— README.md
|        |—— requirements.txt
|        |—— run.sh
|        |—— test
|            |—— test.py
|            |—— __init__.py
|    |—— NotifyService
|        |—— .env
|        |—— app.py
|        |—— DockerFile
|        |—— README.md
|        |—— requirements.txt
|    |—— PolicyService
|        |—— .env
|        |—— app
|            |—— app.py
|            |—— config.py
|            |—— polices
|                |—— policeconfig.py
|                |—— requestenforcer.py
|                |—— __init__.py
|            |—— schemes.py
|            |—— __init__.py
|        |—— Dockerfile
|        |—— policies.yaml
|        |—— README.md
|        |—— requirements.txt
|    |—— TradeService
|        |—— .dockerignore
|        |—— .env
|        |—— app
|            |—— app.py
|            |—— config.py
|            |—— crud.py
|            |—— database
|                |—— database.py
|                |—— __init__.py
|            |—— models
|                |—— models.py
|                |—— __init__.py
|            |—— schemas
|                |—— trade.py
|                |—— __init__.py
|            |—— __init__.py
|        |—— Dockerfile
|        |—— map.html
|        |—— README.md
|        |—— requirements.txt
|        |—— run.sh
|    |—— UserService
|        |—— .dockerignore
|        |—— .env
|        |—— app
|            |—— app.py
|            |—— config.py
|            |—— users
|                |—— database.py
|                |—— models.py
|                |—— router.py
|                |—— schemas.py
|                |—— secretprovider.py
|                |—— usermanager.py
|                |—— __init__.py
|            |—— __init__.py
|        |—— Dockerfile
|        |—— README.md
|        |—— requirements.txt
|        |—— run.sh
|—— Smart-contract
|    |—— DealTracker.sol
```
### Тестируемая платформа 
- software
  ```
  OS: Debian, Windows 11
  Python: 3.11 (venv)
  ```
- hardware
  ```
  RAM: 16 GB
  CPU: Intel I5-8600K 
  GPU: Nvidia RTX4060 (8GB)
  ```

