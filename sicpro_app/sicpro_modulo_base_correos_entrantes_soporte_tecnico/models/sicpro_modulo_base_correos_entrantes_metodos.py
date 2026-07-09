# -*- coding: utf-8 -*-

from odoo import models, fields


class CorreosEntrantesMetodosSoporte(models.Model):
    _inherit = 'sicpro.modulo.base.correos.entrantes.metodos'

    name = fields.Selection(
        selection_add=[
            ('metodo_automatiza_correo_soporte_tecnico', 'APLICACIÓN DE SOPORTE - SOLICITUDES DE SOPORTE TÉCNICO')],
        ondelete={'metodo_automatiza_correo_soporte_tecnico': 'cascade'})
