# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.controller import BaseController, route
from .services import svc_pkgs


class Controller(BaseController):
    @route('/', 'GET')
    async def packages(self, _):
        return jsonify(await svc_pkgs.get_pkgs())

    @route('/<package_name>', 'GET')
    async def package(self, package_name):
        return jsonify(await svc_pkgs.get_pkg(package_name))
