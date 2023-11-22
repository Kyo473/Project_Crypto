import asyncio
import uuid
import unittest
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"WebSocket connected: {websocket}")

    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"WebSocket disconnected: {websocket}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        print(f"Message sent to {websocket}: {message}")

    async def broadcast(self, message: str, RoomID: uuid.UUID, client_id: uuid.UUID, add_to_db: bool):
        if add_to_db:
            # Не добавляем в БД, так как тестируем без реальной БД
            pass

        for connection in self.active_connections:
            await connection.send_text(message)
            print(f"Broadcast message sent to {connection}: {message}")
manager = ConnectionManager() 

class TestConnectionManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.manager = ConnectionManager()

    async def test_connect(self):
        fake_websocket = FakeWebSocket()
        await self.manager.connect(fake_websocket)
        self.assertIn(fake_websocket, self.manager.active_connections)

    async def test_send_personal_message(self):
        fake_websocket = FakeWebSocket()
        await self.manager.send_personal_message("Test message", fake_websocket)

    async def test_broadcast(self):
        fake_websockets = [FakeWebSocket() for _ in range(3)]
        self.manager.active_connections.extend(fake_websockets)
        test_message = "Broadcast test message"
        room_id = uuid.uuid4()
        client_id = uuid.uuid4()
        await self.manager.broadcast(test_message, room_id, client_id, add_to_db=False)
    
    async def test_disconnect(self):  
        fake_websocket = FakeWebSocket()
        self.manager.active_connections.append(fake_websocket)
        await self.manager.disconnect(fake_websocket)
        self.assertNotIn(fake_websocket, self.manager.active_connections)
class FakeWebSocket:
    def __init__(self):
        self.text_to_send = ""
        self.received_texts = []

    async def accept(self):
        pass

    async def send_text(self, text):
        self.received_texts.append(text)

    async def receive_text(self):
        return self.text_to_send

    def disconnect(self):
        pass