import re
import tempfile

import casbin
import jwt
import yaml
from fastapi import Request
from pydantic.dataclasses import dataclass

from app.polices.policeconfig import PoliciesConfig, Policy, Service


@dataclass
class EnforceResult:
    access_allowed: bool = False
    redirect_service: str = None


class RequestEnforcer:
    def __init__(self, config_path: str, jwt_secret: str) -> None:
        self.jwt_secret: str = jwt_secret
        self.config: PoliciesConfig = self.__load_config(config_path=config_path)
        self.enforcer: casbin.Enforcer = self.__create_enforcer()

    def enforce(self, request: Request) -> EnforceResult:
        in_whitelist, service_name = self.__is_request_in_whilelist(request)
        if in_whitelist:
            service = self.__get_service_by_name(service_name)
            return EnforceResult(True, service.entrypoint.unicode_string())

        access_allowed, service_name = self.__check_by_policy(request)
        if access_allowed:
            service = self.__get_service_by_name(service_name)
            return EnforceResult(True, service.entrypoint.unicode_string())
        return EnforceResult()

    def __load_config(self, config_path: str) -> PoliciesConfig:
        with open(config_path) as file:
            data = yaml.safe_load(file)
            return PoliciesConfig(**data)

    def __create_enforcer(self) -> casbin.Enforcer:
        model_conf = self.__make_model_temp_file()
        policy_conf = self.__make_policy_temp_file()
        return casbin.Enforcer(model_conf, policy_conf)

    def __make_model_temp_file(self) -> str:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp.name, 'w') as f:
            f.write(self.config.model)

        return tmp.name

    def __make_policy_temp_file(self) -> str:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        with open(tmp.name, 'w') as f:
            f.writelines(
                list(f'p, {p.rule}, {p.resource}, {p.methods}\n' for p in self.config.policies if not p.white_list)
            )
        return tmp.name

    def __is_request_in_whilelist(self, request: Request) -> tuple[bool, str]:
        resource = '/' + request.path_params['path_name']
        for p in self.whilelist_policies:
            if re.match(p.resource, resource) is not None and request.method in p.method_list:
                return True, p.service
        return False, None   
    
    def __extract_token_data(self, request: Request) -> dict:
        try:
            if 'authorization' in request.headers:
                token = request.headers['authorization'].split(' ')[1]
                return jwt.decode(token, self.jwt_secret, algorithms=["HS256"], audience=["fastapi-users:auth"])
        except:
            return None
        return None
    
    def __check_by_policy(self, request: Request) -> tuple[bool, str]:
        token_data = self.__extract_token_data(request)

        if token_data is None:
            return False, None

        resource = '/' + request.path_params['path_name']

        access_allowed  = self.enforcer.enforce(token_data, resource, request.method)
        if access_allowed is False:
            return False, None

        for p in self.enforcing_policies:
            if re.match(p.resource, resource) is not None and request.method in p.method_list:
                return True, p.service
        
        return True, None

    def __get_service_by_name(self, service_name: str) -> Service:
        for s in self.config.services:
            if s.name == service_name:
                return s
        return None

    @property
    def service_schemes(self) -> list[str]:
        return [s.openapi_scheme for s in self.config.services]

    @property
    def services(self) -> list[Service]:
        return [s for s in self.config.services]


    @property
    def whilelist_resources(self) -> list[str]:
        return [p.resource for p in self.config.policies if p.white_list]
    
    @property
    def whilelist_policies(self) -> list[Policy]:
        return [p for p in self.config.policies if p.white_list]
    
    @property
    def enforcing_policies(self) -> list[Policy]:
        return [p for p in self.config.policies if not p.white_list]