# Сервис проверки полномочий - API Сервис

Этот проект представляет собой точку входа для всех API и сервис для проверки полномочий.

## Запуск проекта
### Для запуска проекта из директории выполните следующие команды:

```bash
docker-compose -f deploy/docker-compose.yaml up -d
```
### Для остановки проекта используйте:

```bash
docker-compose -f deploy/docker-compose.yaml stop
```

# Конфигурация
| Переменная           | Назначение                                               | Значение по-умолчанию     |
| -----------          | -----                                                    | ---                       |
| JWT_SECRET           | Парольная фраза, используемая для кодирования jwt-токена | jwt_secret                |
| POLICIES_CONFIG_PATH | Путь к конфигу политик                                   | policies.yaml             |


# Документация

После запуска доступна документация: http://localhost:5003/docs