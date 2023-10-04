API сервиса управления сделками

Команды
Запуск проекта из директории
docker-compose  -f deploy/docker-compose.yaml up -d
Остановка проекта из директории
docker-compose  -f deploy/docker-compose.yaml stop

Url:
http://localhost:5000/docs

post /trade
Request body Добавляет сделку в базу
{
  "price": 0,
  "currency": "string",
  "description": ""
}

get /trades Возвращает список сделок
Parameters:range

get /trades/{TradeId} Возвращает информацию о сделке
Parameters:id 

put /trades/{TradeId} Обновляет информацию о сделке
Parameters:id 

delete /trades/{TradeId} Удаляет сделку из базы
Parameters:id 

