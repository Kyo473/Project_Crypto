API сервиса управления сделками

формирование контейнеров app и db
docker-compose -f docker-compose.yml up -d
Url:
http://localhost:5000/docs

post /trade
Request body Добавляет сделку в базу
{
  "price": 0,
  "currency": "string",
  "description": "",
  "created_at": "string"
}

get /trades Возвращает список сделок
Parameters:range

get /trades/{TradeId} Возвращает информацию о сделке
Parameters:id 

put /trades/{TradeId} Обновляет информацию о сделке
Parameters:id 

delete /trades/{TradeId} Удаляет сделку из базы
Parameters:id 
