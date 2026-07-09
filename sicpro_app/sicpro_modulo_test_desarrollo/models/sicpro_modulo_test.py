# -*- coding: utf-8 -*-
import base64
from base64 import b64decode

import requests
from cryptography import x509
from cryptography.hazmat import backends
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, pkcs12

from odoo import models, fields
from odoo.tools.safe_eval import json, _logger


class SicproTest(models.Model):
    _name = "sicpro.modulo.test"
    _description = 'Módulo para generar funcionalidades'

    name = fields.Char(string='Nombre', required=False)

    def fun_test_1(self):
        l = 0

    def fun_test_2(self):
        L = 0
