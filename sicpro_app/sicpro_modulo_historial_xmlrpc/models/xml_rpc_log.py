# -*- coding: utf-8 -*-

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class XmlRpcLog(models.Model):
    _name = 'xml.rpc.log'
    _description = 'Historial de solicitudes xmlrpc'

    method = fields.Char(string='Método')
    data = fields.Text(string='Datos')
    model = fields.Char(string='Modelo')
    return_msg = fields.Text(string='Mensaje')
  
    
   
