import logging
import httpx
import websockets
import asyncio
from typing import Any, Dict
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from app import config, schemes
from app.polices.requestenforcer import EnforceResult, RequestEnforcer

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s %(message)s"
)

app_config: config.Config = config.load_config()

policy_checker: RequestEnforcer = RequestEnforcer(
    app_config.policies_config_path, app_config.jwt_secret.get_secret_value()
)

class App(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        scheme_builder = schemes.SchemeBuilder(super().openapi())

        for target in policy_checker.services:
            resp = httpx.get(target.openapi_scheme)
            scheme_builder.append(resp.json(), inject_token_in_swagger=target.inject_token_in_swagger)
        return scheme_builder.result


app = App()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)
async def forward(websocket: WebSocket, client: websockets.WebSocketClientProtocol):
    while True:
        data = await websocket.receive()
        logger.info("Websocket received: %s", data)
        await client.send(data['text'])


async def reverse(websocket: WebSocket, client: websockets.WebSocketClientProtocol):
    while True:
        data = await client.recv()
        logger.info("Websocket sent: %s", data)
        await websocket.send_bytes(data)

@app.websocket("/ws/{path_name:path}")
async def websocket_endpoint(websocket: WebSocket, path_name: str):
    enforce_result = policy_checker.enforce_websocket(websocket, path_name)

    if not enforce_result.access_allowed:
        await websocket.close()
        return

    await websocket.accept()
    async with websockets.connect(f'ws://chat-service:5001/ws/{path_name}') as client:
        fwd_task = asyncio.create_task(forward(websocket, client))
        rev_task = asyncio.create_task(reverse(websocket, client))
        await asyncio.gather(fwd_task, rev_task)

@app.websocket("/proxy/{path_name:path}")
async def websocket_proxy(websocket: WebSocket, path_name: str):
    enforce_result = policy_checker.enforce_websocket(websocket, path_name)

    if not enforce_result.access_allowed:
        await websocket.close()
        return

    await websocket.accept()
    async with websockets.connect(f'ws://chat-service:5001/ws/{path_name}') as client:
        fwd_task = asyncio.create_task(forward(websocket, client))
        rev_task = asyncio.create_task(reverse(websocket, client))
        await asyncio.gather(fwd_task, rev_task)

@app.api_route("/{path_name:path}", methods=["GET", "DELETE", "PATCH", "POST", "PUT", "HEAD", "OPTIONS", "CONNECT", "TRACE"])
async def catch_all(request: Request, path_name: str):
    enforce_result: EnforceResult = policy_checker.enforce(request)
    if not enforce_result.access_allowed:
        logger.info('The user does not have enough permissions. A blocked route: %s', path_name)
        return JSONResponse(content={'message': 'Content not found'}, status_code=404)

    logger.info('The request will be redirected along the route: %s%s', enforce_result.redirect_service, path_name)
    return await redirect_user_request(request, enforce_result)

async def redirect_user_request(request: Request, enforce_result: EnforceResult):
    client = httpx.AsyncClient(base_url=enforce_result.redirect_service)
    url = httpx.URL(path=request.url.path,
                    query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(request.method, url,
                                  headers=request.headers.raw,
                                  content=await request.body())
    rp_resp = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers
    )