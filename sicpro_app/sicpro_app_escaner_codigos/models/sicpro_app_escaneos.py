# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SicproEscaneo(models.Model):
    _name = 'sicpro.app.codigos.escaneados'
    _description = 'Registro de códigos escaneados'

    nombre_modelo = fields.Char(string='Modelo', size=64, )
    identificador = fields.Integer(string='Identificador', )
    nombre_elemento = fields.Char(string='Nombre de Material', )
