# -*- coding: utf-8 -*-

from jetfactory import JetfactoryException, jetmgr
from jetfactory.service import VanillaService
from jetfactory.utils import format_path


class PackageService(VanillaService):
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
            # meta = schema_fields = []
            schema_fields = []

            if route.schema:
                schema_fields = [f async for f in self.fields_by_schema(route.schema)]
                # if hasattr(schema, 'Meta'):
                #    meta = route.schema.Meta

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
            path=format_path(self.sanic.config['API_BASE'], pkg.controller.path),
            routes=[r async for r in self.routes(pkg.controller)]
        )

    async def get_pkg(self, name):
        pkg = jetmgr.get_pkg(name)
        if not pkg:
            raise JetfactoryException(f'Unknown package', 404)

        return await self.pkg_extended(pkg)

    async def get_pkgs(self):
        return [await self.pkg_extended(pkg) for _, pkg in jetmgr.pkgs]


"""
cls.openapi = pkg.spec.plugins[0].openapi
from apispec.ext.marshmallow.openapi import OpenAPIConverter
openapi: OpenAPIConverter

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

"""
