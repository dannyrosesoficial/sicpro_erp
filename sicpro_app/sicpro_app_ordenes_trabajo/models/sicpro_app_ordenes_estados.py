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


class OrdenesEstados(models.Model):
    _name = "sicpro.app.ordenes.estados"
    _description = "Estado de las órdenes de trabajo"
    _rec_name = 'name'
    _order = "sequence asc"

    name = fields.Char(string='Nombre del estado', required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    is_fecha_inicial = fields.Boolean(string='Necesaria fecha inicial')
    is_preparacion_tecnica = fields.Boolean(
        string='Etapa Preparación T.')
    is_en_proceso = fields.Boolean(string='Etapa de Ejecución')
    is_terminada = fields.Boolean(string='Etapa Terminada')
    is_paralizado = fields.Boolean(string='Etapa Paralizada')
    is_cancelado = fields.Boolean(string='Etapa Cancelada')
    requirements = fields.Text(string='Requerimientos')
    fold = fields.Boolean(string='Replegado', )
    company_id = fields.Many2one('res.company', string='Proceso Ejecutor',
                                 domain="[('ejecuta_proceso', '=', True)]",
                                 required=True, )
    company_abreviatura = fields.Char(string='Abreviatura',
                                      related='company_id.identificador_corto')
    active = fields.Boolean(string='Activo', default=True)

    # --- CONTROL DE EXCLUSIVIDAD DE ETAPAS ---
    @api.constrains('is_preparacion_tecnica', 'is_en_proceso', 'is_terminada',
                    'is_paralizado', 'is_cancelado')
    def _check_flags_mutually_exclusive(self):
        """ Asegura que un estado no sea asignado a dos etapas críticas a la vez """
        for record in self:
            flags = [record.is_preparacion_tecnica, record.is_en_proceso,
                record.is_terminada, record.is_paralizado, record.is_cancelado]
            # Contamos cuántas banderas se marcaron como True
            if flags.count(True) > 1:
                raise ValidationError("Error de configuración en SICPRO:\n"
                                      "Un estado de orden de trabajo no puede pertenecer a múltiples etapas críticas simultáneamente "
                                      "(Preparación, Ejecución, Terminada, Paralizada o Cancelada).\n\n"
                                      "Por favor, defina una única función "
                                      "operativa para el estado '%s'." % record.name + MSG_SOPORTE_SICPRO)