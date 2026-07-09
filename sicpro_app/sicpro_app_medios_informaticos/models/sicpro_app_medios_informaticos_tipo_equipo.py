# -*- coding: utf-8

from odoo import models, fields


class MediosInformaticosTipoEquipo(models.Model):
    _name = 'sicpro.app.medios.informaticos.tipo.equipo'
    _description = "Tipo de Medio Informático"

    name = fields.Char('Tipo de Equipo', required=True, )
    active = fields.Boolean('Activo', default=True)
    imagen = fields.Image('Imagen')

    _sql_constraints = [('name_uniq', 'unique (name)', "¡El Tipo Equipo ya existe!"), ]
