# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.controller import BaseController, route
from .service import APISpecService


class Controller(BaseController):
    def __init__(self):
        self.service = APISpecService()

    @route('/', 'GET')
    async def visits_get(self, _):
        return jsonify(await self.service.get_pkgs())

    @route('/<package_name>', 'GET')
    async def package_get(self, package_name):
        return jsonify(await self.service.get_pkg(package_name))
