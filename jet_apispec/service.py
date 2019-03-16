# -*- coding: utf-8 -*-

from jetfactory import jetmgr
from jetfactory.service import BaseService
from ._apispec import ApiSpec


class APISpecService(BaseService):
    pkgs = {}

    def on_ready(self):
        self._generate_specs()

    def _generate_specs(self):
        for name, pkg in jetmgr.pkgs:
            spec = ApiSpec(pkg)

            for route_stack in pkg.controller.stacks:
                spec.consume_stack(*route_stack)

            self.pkgs[name] = spec.schema

    async def get_pkgs(self):
        return self.pkgs.values()

    async def get_pkg(self, name):
        return self.pkgs[name]
