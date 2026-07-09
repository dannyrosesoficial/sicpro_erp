# -*- coding: utf-8 -*-

from odoo import fields, models


class NomencladorEspecialidades(models.Model):
    _inherit = 'sicpro.nomenclador.especialidad'

    departamento = fields.Many2one('sicpro.app.trabajadores.departmentos',
                                   string="Departamento", required=False, )
