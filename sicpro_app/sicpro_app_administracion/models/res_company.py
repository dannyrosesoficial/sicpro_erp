# -*- coding: utf-8 -*-


from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'
    _order = 'id'

    identificador_corto = fields.Char(string="Identificador", required=True, )
    ejecuta_proceso = fields.Boolean(string="Ejecutor de Procesos", )
    login_redes_sociales = fields.Boolean(string="Redes Sociales", default=False)
