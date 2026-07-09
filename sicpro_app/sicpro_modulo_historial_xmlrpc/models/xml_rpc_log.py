# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class XmlRpcLog(models.Model):
    _name = 'xml.rpc.log'
    _description = 'Historial de solicitudes xmlrpc'
    _rec_name = 'method'
    _order = 'create_date desc'

    method = fields.Char(string='Método')
    data = fields.Text(string='Datos')
    model = fields.Char(string='Modelo')
    return_msg = fields.Text(string='Mensaje')

    @api.model_create_multi
    def create(self, vals_list):
        _logger.debug("Creando xml.rpc.log para %d elementos", len(vals_list))
        records = super(XmlRpcLog, self).create(vals_list)
        _logger.info("Se crearon %d registros de xml.rpc.log", len(records))
        return records



