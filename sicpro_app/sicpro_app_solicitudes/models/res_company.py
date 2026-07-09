# -*- coding: utf-8 -*-


from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'
    _order = 'id'

    jefe_proceso = fields.Many2one(comodel_name='sicpro.app.trabajadores', string='Jefe del Proceso', required=False)
