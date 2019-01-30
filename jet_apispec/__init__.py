# -*- coding: utf-8 -*-

from jetfactory import Jetpack
from .controller import Controller
from .services import svc_pkgs

__jetpack__ = Jetpack(
    name='apispec',
    description='OpenAPI specification generator',
    controller=Controller,
    services=[svc_pkgs],
    models=[]
)
