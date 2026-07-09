# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrabajadoresClavesHorasLabor(models.Model):
    _name = 'sicpro.app.trabajadores.claves.horas'
    _description = 'Claves de Horas Trabajador'

    name = fields.Char(required=True, string='Claves')
    descripcion = fields.Char(string="Descripción", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
