# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrDepartment(models.Model):
    _inherit = 'survey.user_input'

    trabajador_id = fields.Many2one('sicpro.app.trabajadores',
                                    string='Trabajador', required=False)
