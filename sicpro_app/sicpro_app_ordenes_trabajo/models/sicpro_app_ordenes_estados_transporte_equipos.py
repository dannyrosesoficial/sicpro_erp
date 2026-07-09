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


class OrdenesEstadosTransporteEquipos(models.Model):
    _name = "sicpro.app.ordenes.estados.transporte.equipos"
    _description = "Estado del transporte y los equipos en las obras"
    _rec_name = 'name'
    _order = "sequence asc"

    name = fields.Char(string='Nombre del estado', required=True)
    tipo = fields.Selection(string='Tipo',
                            selection=[('vehiculo', 'Vehículos'), (
                            'equipo_especializado', 'Equipos Especializados'),
                                       ('equipo_complementario',
                                        'Equipos Complementarios'), ],
                            required=True, )
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    detalles = fields.Text(string='Detalles')
    active = fields.Boolean(string='Activo', default=True, index=True)
    contar = fields.Boolean(string='Contar', default=False)

    # --- CONTROL DE UNICIDAD POR TIPO DE EQUIPAMIENTO ---
    @api.constrains('name', 'tipo')
    def _check_name_type_uniqueness(self):
        """ Garantiza que no existan estados duplicados dentro de la misma categoría de transporte/equipo """
        for record in self:
            if record.name and record.tipo:
                duplicate = self.search(
                    [('name', '=', record.name), ('tipo', '=', record.tipo),
                        ('id', '!=', record.id)], limit=1)

                if duplicate:
                    # Obtenemos la etiqueta legible del Selection para el mensaje de error
                    tipo_label = dict(self._fields['tipo'].selection).get(
                        record.tipo)
                    raise ValidationError(
                        "¡Configuración duplicada en SICPRO!\n\n"
                        "El estado '%s' ya se encuentra registrado para la categoría de '%s'. "
                        "Por favor, use un nombre diferente o edite el estado existente." % (
                        record.name, tipo_label) + MSG_SOPORTE_SICPRO)