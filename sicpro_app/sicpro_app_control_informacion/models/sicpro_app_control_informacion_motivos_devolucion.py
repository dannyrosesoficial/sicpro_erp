# -*- coding: utf-8 -*-

from odoo import fields, models


class ControlInformacionMotivosRechazos(models.Model):
    _name = "sicpro.app.control.informacion.motivos.devolucion"
    _description = "Motivos de rechazo del control de información"

    name = fields.Char('Motivo', required=True)
    active = fields.Boolean('Activo', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "El motivo de rechazo ya existe!"),
    ]
