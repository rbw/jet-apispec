# -*- coding: utf-8 -*-

from jetfactory.utils import jsonify
from jetfactory.controller import BaseController, route
from .services import svc_pkgs


class Controller(BaseController):
    @route('/packages', 'GET', inject_request=False)
    async def packages(self):
        return jsonify(await svc_pkgs.get_pkgs())

    @route('/packages/<package_name>', 'GET')
    async def package(self, package_name):
        return jsonify(await svc_pkgs.get_pkg(package_name))
