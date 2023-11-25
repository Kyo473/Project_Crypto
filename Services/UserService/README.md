# API сервиса управления пользователями

Реализован на основе фреймворка [fastapi-users](https://fastapi-users.github.io/)

# Зависимости

Перед запуском сервиса необходимо установить зависимости из файла requirements.txt

# Для запуска проекта из директории выполните следующие команды:

```bash
docker-compose -f deploy/docker-compose.yaml up -d
```
# Для остановки проекта используйте:
```bash
docker-compose -f deploy/docker-compose.yaml stop
```
## API Управления пользователями :
    - `POST` **/auth/register** - creating a new user account
    - `POST` **/auth/jwt/login** - user login
    - `POST` **/auth/jwt/logout** - user logout
    - `GET` **/users/me** - getting information about the current user
    - `GET` **/users/{id}** - obtaining information about a specific user
    - `PATCH` **/users/me** - updating information about the current user
    - `PATCH` **/users/{id}** - updating information about a specific user (available only to administrators)
    - `DELETE` **users/{id}** - deleting a user (available only to administrators)
# Запуск с использование файла конфигурации .env

Для запуска из файла конфигурации нужно поместить файл .env в корень сервиса

# Конфигурация
| Переменная                  | Назначение                                                         | Значение по-умолчанию                        |
| -----------                 | -----                                                              | ---                                          |
| POSTGRES_DSN                | Строка подключения к PostgreSQL                                    | postgresql://user:pass@localhost:5432/foobar |
| JWT_SECRET                  | Парольная фраза, используемая для кодирования jwt-токена           | jwt_secret                                   | 
| RESET_PASSWORD_TOKEN_SECRET | Парольная фраза, используемая для кодирования токена сброса пароля | reset_password_token_secret                  | 
| VERIFICATION_TOKEN_SECRET   | Парольная фраза, используемая для кодирования токена верификации   | verification_token_secret                    | 

# Документация

После запуска доступна документация: http://localhost:5002/docs
