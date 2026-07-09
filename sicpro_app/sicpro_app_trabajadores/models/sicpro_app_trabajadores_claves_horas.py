# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class TrabajadoresClavesHorasLabor(models.Model):
    _name = 'sicpro.app.trabajadores.claves.horas'
    _description = 'Claves de Horas Trabajador'

    name = fields.Char(required=True, string='Claves')
    descripcion = fields.Char(string="Descripción", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
