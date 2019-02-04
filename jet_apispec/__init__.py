# -*- coding: utf-8 -*-

from jetfactory import Jetpack
from .app import svc_apispec, controller

__version__ = '0.1.0'

APP = Jetpack(
    name='apispec',
    description='OpenAPI specification generator',
    controller=controller,
    services=[svc_apispec],
    models=[],
)
