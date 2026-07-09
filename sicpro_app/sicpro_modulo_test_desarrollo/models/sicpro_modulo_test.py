# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import base64
from base64 import b64decode

import requests
from cryptography import x509
from cryptography.hazmat import backends
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, pkcs12

from odoo import models, fields
from odoo.tools.safe_eval import json, _logger
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO


class SicproTest(models.Model):
    _name = "sicpro.modulo.test"
    _description = 'Módulo para generar funcionalidades'

    name = fields.Char(string='Nombre', required=False)

    def fun_test_1(self):
        l = 0
        raise ValidationError("La abreviatura es obligatoria para las provincias de Cuba.\n\n" + MSG_SOPORTE_SICPRO)


    def fun_test_2(self):
        L = 0
