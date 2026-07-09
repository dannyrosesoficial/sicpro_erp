# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO

PRIORIDADES_ACTIVAS = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
    ('3', 'Muy Alta'), ]


class OrdenesEstadosTrabajador(models.Model):
    _name = "sicpro.app.ordenes.estados.trabajador"
    _description = "Estado de los trabajadores en las obras"
    _rec_name = 'name'
    _order = "sequence asc"

    name = fields.Char(string='Nombre del estado', required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    detalles = fields.Text(string='Detalles')
    active = fields.Boolean(string='Activo', default=True, index=True)
    contar = fields.Boolean(string='Contar', default=False)

    @api.constrains('name')
    def _check_name_uniqueness(self):
        """ Evita la duplicación de nombres de estados de trabajadores en las obras """
        for record in self:
            if record.name:
                duplicate = self.search(
                    [('name', '=', record.name), ('id', '!=', record.id)],
                    limit=1)

                if duplicate:
                    raise ValidationError(
                        "¡El nombre del estado del trabajador ya existe en el sistema!\n\n"
                        "Por favor, defina una etiqueta diferente para no causar confusiones en el control del personal." + MSG_SOPORTE_SICPRO)