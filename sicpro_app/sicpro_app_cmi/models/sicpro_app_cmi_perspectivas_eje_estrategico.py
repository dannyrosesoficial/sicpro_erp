# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from random import randint
import base64
from odoo import api, Command, fields, models, modules
from odoo.exceptions import UserError


def _default_color():
    return randint(1, 11)


class AppCMIPerspectivasEjeEstrategico(models.Model):
    _name = 'sicpro.app.cmi.perspectivas.eje.estrategico'
    _order = "id asc"
    _description = 'Ejes Estratégicos del CMI'



    name = fields.Char(string='Nombre', required=True)
    user_id = fields.Many2one('res.users', string='Usuario', index=True,
                              default=lambda self: self.env.uid)
    descripcion = fields.Char(string="Descripción", required=True, )
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    active = fields.Boolean(string="Activo", default=True, index=True)
    anio = fields.Char(string="Año", required=True,
                       default=fields.Datetime.now().strftime("%Y"), )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
