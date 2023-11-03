class SchemeBuilder:
    def __init__(self, source_scheme: dict) -> None:
        self.__result: dict = source_scheme
        self.__result['paths'] = {}
        self.__result['components']['securitySchemes'] = {}

    def append(self, scheme: dict, inject_token_in_swagger = False):
        if 'components' in scheme and 'schemas' in scheme['components']:
            self.__result['components']['schemas'].update(scheme['components']['schemas'])
        if 'components' in scheme and 'securitySchemes' in scheme['components']:
            self.__result['components']['securitySchemes'].update(scheme['components']['securitySchemes'])
        if 'paths' in scheme:
            paths = scheme['paths']
            if inject_token_in_swagger:
                for _, p in paths.items():
                    for k, v in p.items():
                        p[k]['security'] = [{"OAuth2PasswordBearer": []}]
            self.__result['paths'].update(paths)

    @property
    def result(self):
        return self.__result