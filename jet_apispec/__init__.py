# -*- coding: utf-8 -*-

from jetfactory import Jetpack
from .controller import Controller
from .service import APISpecService

__version__ = '0.1.0'

export = Jetpack(
    name='apispec',
    description='OpenAPI specification generator',
    controller=Controller,
    services=[APISpecService],
    models=[],
)
