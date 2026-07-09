# -*- coding: utf-8 -*-

from odoo import models, fields


class TrabajadoresDocumentosTipos(models.Model):
    _name = 'sicpro.app.trabajadores.documentos.tipos'
    _description = 'Tipos de documentos del trabajador'

    name = fields.Char(string="Nombre", required=True)
