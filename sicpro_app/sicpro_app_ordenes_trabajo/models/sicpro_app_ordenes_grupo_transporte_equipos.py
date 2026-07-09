# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError

PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta'), ]


class OrdenesGrupoTransporte(models.Model):
    _name = "sicpro.app.ordenes.grupo.transporte"
    _description = "Grupos del transporte"
    _rec_name = 'grupoEquipoNombre'
    _auto = False  # significa que se basa en una vista SQL

    grupoEquipoNombre = fields.Char(string="Grupo", readonly=True)
    color = fields.Integer(string='Color', readonly=True)

    def init(self):
        """ Inicializa la vista SQL asegurando que el color sea pseudoaleatorio pero estático por grupo """
        self.env.cr.execute("""
            DROP VIEW IF EXISTS sicpro_app_ordenes_grupo_transporte;
            CREATE OR REPLACE VIEW sicpro_app_ordenes_grupo_transporte AS (
                SELECT 
                    MIN(id) AS id, 
                    "grupoEquipoNombre", 
                    (ABS(HASHTEXT("grupoEquipoNombre")) % 11) + 1 AS color
                FROM sicpro_app_transporte_general
                WHERE "grupoEquipoNombre" IS NOT NULL
                GROUP BY "grupoEquipoNombre"
            )
        """)


class OrdenesGrupoTransporteEquipos(models.Model):
    _name = "sicpro.app.ordenes.grupo.transporte.equipos"
    _description = "Configuración del transporte y los equipos"
    _rec_name = 'name'
    _order = "sequence asc"

    name = fields.Selection(string='Tipo',
                            selection=[('vehiculo', 'Vehículos'), (
                            'equipo_especializado', 'Equipos Especializados'),
                                       ('equipo_complementario',
                                        'Equipos Complementarios'), ],
                            required=True, )
    grupo_vehiculos = fields.Many2many("sicpro.app.ordenes.grupo.transporte",
                                       'sicpro_app_ordenes_grupos_trasporte_rel',
                                       'nombre_id', 'grupo_id',
                                       string="Grupo vehículos",
                                       required=True, )
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    detalles = fields.Text(string='Detalles')
    active = fields.Boolean(string='Activo', default=True, index=True)

    @api.constrains('name', 'active')
    def _check_tipo_unico(self):
        """ Valida de forma segura para multi-registros que el tipo sea único si está activo """
        for record in self:
            if record.active and record.name:
                # Odoo asume el operador AND por defecto, limpiamos los selectores prefijados
                duplicate = self.search(
                    [("active", "=", True), ("name", "=", record.name),
                        ("id", "!=", record.id)], limit=1)

                if duplicate:
                    # Obtenemos el texto legible del tipo para un mejor feedback al usuario
                    tipo_label = dict(self._fields['name'].selection).get(
                        record.name)
                    raise ValidationError(
                        f"¡El tipo operativo '{tipo_label}' ya se encuentra configurado y activo en el sistema!.\n\n"
                        f"{MSG_SOPORTE_SICPRO}")