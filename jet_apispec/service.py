# -*- coding: utf-8 -*-

from functools import lru_cache

from apispec import APISpec
from apispec.ext.marshmallow import OpenAPIConverter, MarshmallowPlugin

from jetfactory import jetmgr
from jetfactory.exceptions import JetfactoryException
from jetfactory.service import BaseService
from jetfactory.utils import format_path


class APISpecService(BaseService):
    @staticmethod
    async def fields_by_schema(schema):
        for field_name, field in schema.declared_fields.items():
            yield dict(
                name=field_name,
                type=field.__class__.__name__,
                required=field.required,
                load_only=field.load_only,
                dump_only=field.dump_only,
            )

    async def routes(self, controller):
        for handler_name, (path, route) in dict(controller.routes).items():
            schema_fields = []

            if route.schema:
                schema_fields = [f async for f in self.fields_by_schema(route.schema)]

            yield dict(
                handler=handler_name,
                path=path,
                method=route.method,
                fields=schema_fields,
                doc=route.doc
            )

    async def pkg_extended(self, pkg):
        return dict(
            name=pkg.name,
            summary=pkg.meta.get('summary'),
            description=pkg.meta.get('description'),
            path=format_path(self.app.config['API_BASE'], pkg.controller.path),
            routes=[r async for r in self.routes(pkg.controller)]
        )

    @lru_cache()
    def get_pkg_spec(self, name, pkg):
        api_spec = APISpec(
            title=name.capitalize(),
            info={
                'description': pkg.description,
            },
            version=pkg.version,
            openapi_version='3.0.2',
            plugins=[MarshmallowPlugin()]
        )

        return api_spec, api_spec.plugins[0].openapi

    async def get_pkgs(self):
        for name, pkg in jetmgr.pkgs:
            api_spec, openapi = self.get_pkg_spec(name, pkg)

            for handler_name, (path_full, route, schema) in dict(pkg.controller.routes).items():
                if not schema:
                    continue

                endpoint = {
                    'summary': 'test',
                    'operationId': handler_name,
                    'tags': '',
                    'parameters': openapi.schema2parameters(schema)
                }

                print(openapi.schema2jsonschema(schema))

            #for handler_name, route in dict(pkg.controller.routes).items():
            #    print(route)

    async def get_pkg(self, name):
        endpoint = {
            'summary': 'test',
            'operationId': handler.__name__,
            'tags': '',
            'parameters': []
        }

        schemas = {}

        for group, field in schema.declared_fields.items():
            if group == 'response':
                field.dump_only = True
                schemas[schema.__class__.__name__] = self.openapi.field2property(field, name=group)
                continue
            elif group == 'body':
                field.load_only = True

            endpoint['parameters'].append(self.openapi.field2property(field, name=group))

            # data = self.openapi.field2property(field, name=group)

        pprint(schemas)

        if route.path in data:
            data[route.path].update({route.method: endpoint})
        else:
            data[route.path] = {route.method: endpoint}

