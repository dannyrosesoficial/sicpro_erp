# -*- coding: utf-8 -*-

from odoo import fields, models


class TrabajadoresDepGeneral(models.Model):
    _inherit = 'sicpro.app.trabajadores.general'

    equipo_ejecutor_id = fields.Many2one(
        comodel_name='sicpro.app.solicitudes.grupo.ejecutor',
        string="Equipo Ejecutor", required=False, )
