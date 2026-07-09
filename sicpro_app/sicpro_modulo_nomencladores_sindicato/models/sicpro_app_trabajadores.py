# -*- coding: utf-8 -*-

from random import randint

from odoo import models, fields


def _default_color():
    return randint(1, 11)


class TrabajadoresGeneral(models.Model):
    _inherit = 'sicpro.app.trabajadores'

    seccion_sindical_id = fields.Many2one("sicpro.nomenclador.sindicato", string="Sección Sindical",
                                          related='area_id.seccion_sindical_id', tracking=True)
