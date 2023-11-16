import urllib.parse
from pydantic import BaseModel, HttpUrl

class Service(BaseModel):
    name: str
    entrypoint: HttpUrl
    inject_token_in_swagger: bool = False

    @property
    def openapi_scheme(self) -> str:
        return urllib.parse.urljoin(
            self.entrypoint.unicode_string(), 'openapi.json'
        ) 

class Policy(BaseModel):
    service: str
    rule: str = None
    resource: str
    methods: str
    white_list: bool = False

    @property
    def method_list(self) -> list[str]:
        available_methods = ["GET", "DELETE", "PATCH", "POST", "PUT", "HEAD", "OPTIONS", "CONNECT", "TRACE","WEBSOCKET"]
        return [m for m in available_methods if m in self.methods]


class PoliciesConfig(BaseModel):
    services: list[Service]
    model: str
    policies: list[Policy]