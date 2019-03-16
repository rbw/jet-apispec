# -*- coding: utf-8 -*-


class ApiSpec:
    _routes = None

    def __init__(self, pkg):
        self.version = pkg.version
        self.title = pkg.name.capitalize()
        self.description = pkg.description.capitalize()
        self.servers = [
            {
                'url': 'make_configurable_in_spec_pkg'
            }
        ],
        self.contact = {
            'author': 'get_from_pkg',
            'email': 'get_from_pkg',
        }

        self._routes = {}

    def get_params(self, schema):
        for field_name, field in schema.declared_fields.items():
            yield {
                'name': field_name,
                'in': 'query',
                'description': '',
                'required': field.required,
                'schema': {
                    'type': field.__class__.__name__.lower()
                }
            }

    def get_response(self, schema):
        fields = {}
        load_only = schema.Meta.load_only

        # Uses protected _declared_fields for Nested recursion compatibility
        for field_name, field in schema._declared_fields.items():
            if field_name in load_only:
                continue

            if hasattr(field, 'nested'):
                fields[field_name] = self.get_response(field.nested)
                continue

            fields[field_name] = dict(type=field.__class__.__name__)

        response = {
            'required': [],
            'type': 'object',
            'properties': fields
        }

        if hasattr(schema, 'many') and schema.many:
            return {
                'type': 'array',
                'items': {
                    'allOf': [response]
                }
            }

        return response

    def consume_stack(self, handler, route_stack):
        schemas = route_stack.schemas
        definition = {}

        if route_stack.path not in self._routes:
            self._routes[route_stack.path] = {}

        if schemas['query']:
            params = self.get_params(schemas['query'])
            definition['parameters'] = list(params)

        if schemas['response']:
            response = self.get_response(schemas['response'])
            definition['responses'] = {
                '200': dict(
                    description='',
                    content={'application/json': dict(schema=response)}
                )
            }

        self._routes[route_stack.path].update({
            route_stack.method: {
                'description': route_stack.description,
                'operationId': handler.__name__,
                **definition,
            }
        })

    @property
    def schema(self):
        schema = self.__dict__
        routes = schema.pop('_routes')

        return {
            **schema,
            'paths': routes
        }
