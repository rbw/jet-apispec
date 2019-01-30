# -*- coding: utf-8 -*-

from jetfactory import Jetpack
from jet_apispec.controller import Controller
from jet_apispec.services import svc_pkgs

pkg = Jetpack(
    name='apispec',
    description='OpenAPI specification generator',
    controller=Controller,
    services=[svc_pkgs],
    models=[]
)
