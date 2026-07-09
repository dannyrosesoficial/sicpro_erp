# -*- coding: utf-8 -*-

from odoo import fields, models


class SolicitudesRechazadas(models.Model):
    _name = 'sicpro.app.solicitudes.rechazadas'
    _description = 'Motivo de rechazo'

    name = fields.Char('Descripción', required=True, translate=True)
    active = fields.Boolean('Active', default=True)
