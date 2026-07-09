# -*- coding: utf-8

from odoo import models, fields


class MediosInformaticosTipoEquipo(models.Model):
    _name = 'sicpro.app.medios.informaticos.tramites'
    _description = "Trámites del taller de Medio Informático"

    name = fields.Char('Trámite', required=True)
    active = fields.Boolean('Activo', default=True)

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El Trámite ya existe!"), ]
