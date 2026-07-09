# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class SicproLdapHistorial(models.Model):
    _name = 'sicpro.app.modulo.ldap.historial'
    _description = 'Historial de Registros LDAP'
    _order = 'id desc'

    name = fields.Char(string="Unidades Organizativas", required=True, )
    fecha = fields.Datetime(string='Fecha', required=False)
    registros_creados = fields.Integer(string='Creados', required=False)
    registros_actualizados = fields.Integer(string='Actualizados',
                                            required=False)
    registros_archivados = fields.Integer(string='Archivados', required=False)
    estado = fields.Selection(string='Estado', required=False,
                              selection=[('exito', 'Éxito'),
                                         ('fallido', 'Fallido'), ])
