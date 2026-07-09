# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import random


Prioridades_Activas = [
    ('0', 'Baja'),
    ('1', 'Media'),
    ('2', 'Alta'),
    ('3', 'Muy Alta'),
]


class OrdenesGrupoTransporte(models.Model):
    _name = "sicpro.app.ordenes.grupo.transporte"
    _description = "Grupos del transporte"
    _rec_name = 'grupoEquipoNombre'
    _auto = False  # significa que se basa en una vista SQL

    grupoEquipoNombre = fields.Char("Grupo", readonly=True)
    color = fields.Integer(string='Color', readonly=True)

    def init(self):
        self._cr.execute("""
            DROP VIEW IF EXISTS sicpro_app_ordenes_grupo_transporte;
            CREATE OR REPLACE VIEW sicpro_app_ordenes_grupo_transporte AS (
                SELECT MIN(id) AS id, "grupoEquipoNombre", FLOOR(RANDOM() * 12) AS color
                FROM sicpro_app_transporte_general
                WHERE "grupoEquipoNombre"
                IS NOT NULL
                GROUP BY "grupoEquipoNombre"
                )
        """)

class OrdenesGrupoTransporteEquipos(models.Model):
    _name = "sicpro.app.ordenes.grupo.transporte.equipos"
    _description = "Configuración del transporte y los equipos"
    _rec_name = 'name'
    _order = "sequence asc"

    name = fields.Selection(
        string='Tipo',
        selection=[('vehiculo', 'Vehículos'), ('equipo_especializado', 'Equipos Especializados'),
                   ('equipo_complementario', 'Equipos Complementarios'), ], required=True, )
    grupo_vehiculos = fields.Many2many("sicpro.app.ordenes.grupo.transporte", 'sicpro_app_ordenes_grupos_trasporte_rel',
                                       'nombre_id', 'grupo_id', string="Grupo vehículos", required=True,)
    sequence = fields.Integer('Secuencia', default=1,)
    detalles = fields.Text('Detalles')
    active = fields.Boolean('Activo', default=True)

    @api.constrains('name')
    def _check_tipo_unico(self):
        uniq = self.env['sicpro.app.ordenes.grupo.transporte.equipos'].search(
            ['&', '&', ("active", "=", True), ("name", "=", self.name), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡El tipo introducido ya existe!. "
                                    "Si cree que es un error contacte al administrador"))