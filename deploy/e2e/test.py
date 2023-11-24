import unittest
import pydantic
import requests
import uuid 
import logging
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from datetime import datetime
from enum import Enum
ENTRYPOINT = 'http://policy-enforcement-service:5003/'
TRADE_ENDPOINT = 'http://trade-service:5000/'
DATABASE_DSN = 'postgresql://tradedb:tradedb@Tradedb:5432/tradedb'
ACCESS_DENIED_MESSAGE = {"message": "Content not found"}
# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s %(message)s"
)
class Currency(str,Enum):
    Bitcoin = "BTC"
    Matic = "MATIC"
    USDT = "USDT"
class Status(str,Enum):
    Create = "Create"
    Pending = "Pending"
    Successful = "Successful"
    Appilation = "Appilation"
    Error = "Error"
    

class Trade(pydantic.BaseModel):
    id: uuid.UUID
    buyer_address: str
    seller_address: str   
    price: float
    currency: Currency
    created_at: datetime
    description: str
    lat: float
    lon: float
    hide: Status


class User(pydantic.BaseModel):
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class TestBaseUtils(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_service_available(self):
        response = requests.get(ENTRYPOINT,timeout=15)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)



class TestTradeBase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_trades: List[Trade] = []
        self.trade_id = None
    def setUp(self, seller_id: uuid.UUID, seller_address: str,description:str) -> None:
        self._test_create_trade(seller_id=seller_id,seller_address=seller_address,description=description)
    def tearDown(self) -> None:
        self._delete_trade()


    def _test_create_trade(self, seller_id: uuid.UUID, seller_address: str, description: str):
        payload = {
            "seller_id": seller_id,
            "seller_address": seller_address,
            "price": 33,
            "currency": "BTC",
            "description": description,
            "lat": 54,
            "lon": 45,
            "hide": "Create"
        }
        try:
            response = requests.post(f'{TRADE_ENDPOINT}trade', json=payload,timeout=15)
            self.assertEqual(response.status_code, 201)
            new_trade = Trade(**response.json())
            self.test_trades.append(new_trade)  
            # logger.info("Trade Create")
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)
        
    def _delete_trades(self):
        if not self.test_trades:
            return
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            for trade in self.test_trades:
                delete_query = text("DELETE FROM trades WHERE id = :trade_id")
                # Передача параметра через словарь
                connection.execute(delete_query, {"trade_id": str(trade.id)})
                # logger.info("Trade Delete")
            connection.commit()

    
    def tearDown(self) -> None:
        self._delete_trades()  

   
class TestTrade(TestTradeBase):
    def setUp(self) -> None:
        super().setUp("3fa85f64-5717-4562-b3fc-2c963f66afa6", "test","fast")

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_trades(self):
        response = requests.get(f"{TRADE_ENDPOINT}trades",timeout=15)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data,list)

    def test_get_trade_by(self):
        response = requests.get(f"{TRADE_ENDPOINT}trades/{self.test_trades[0].id}",timeout=15)  
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, dict)



if __name__ == '__main__':
    unittest.main()