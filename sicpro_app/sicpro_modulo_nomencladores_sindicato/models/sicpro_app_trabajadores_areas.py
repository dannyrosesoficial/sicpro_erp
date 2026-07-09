# -*- coding: utf-8 -*-

from random import randint

from odoo import fields, models


def _default_color():
    return randint(1, 11)


class Departamentos(models.Model):
    _inherit = "sicpro.app.trabajadores.areas"

    seccion_sindical_id = fields.Many2one("sicpro.nomenclador.sindicato", string="Sección Sindical", tracking=True)
