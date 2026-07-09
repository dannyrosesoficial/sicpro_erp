# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class TransferenciasGastosOrdenesEstados(models.Model):
    _name = "sicpro.app.transferencias.gastos.ordenes.estados"
    _description = "Estado de los gastos de órdenes de trabajo"
    _order = "sequence asc"

    name = fields.Char(string='Nombre del estado', required=True)
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    fold = fields.Boolean(string='Replegado en la vista Kanban')
    active = fields.Boolean(string='Activo', default=True, index=True)
    inicial = fields.Boolean(string='Estado Inicial', required=False,
                             default=False)
    cron_morosidad = fields.Boolean(string='Revisión de Morosidad',
                                    required=False, default=False)
    terminado = fields.Boolean(string='Estado Terminado', required=False,
                               default=False)
    devuelto_economia = fields.Boolean(string='Devuelto a Economía',
                                       required=False, default=False)
    color_barra = fields.Selection(string='Barra de Color',
                                   selection=[('info', 'Informativo'),
                                              ('warning', 'Atención'),
                                              ('danger', 'Cuidado'),
                                              ('success', 'Completado'), ],
                                   required=True)
    rol_interno = fields.Selection(string='Rol Interno', required=True,
                                   selection=[('dtp', 'DTP'),
                                              ('ejecutores', 'Ejecutores'), (
                                              'inversionistas',
                                              'Inversionistas'),
                                              ('economia', 'Economía'), ])
    valor_tecnico_gastos = fields.Selection(string='Valor Técnico de Gastos',
        required=True, copy=False,
        selection=[('revision_dtp', 'Gastos CJ74 - Revisión Técnico'), (
        'validacion_ejecutor', 'Gastos CJ74 - Validación Ejecutor'),
                   ('rechazado_ejecutor', 'Gastos CJ74 - Rechazado Ejecutor'),
                   ('validacion_inversionista',
                    'Gastos CJ74 - Validación Inversionista'), (
                   'rechazado_inversionista',
                   'Gastos CJ74 - Rechazado Inversionista'), (
                   'espera_contabilizar',
                   'Gastos CJ74 - En Espera por Contabilizar'), (
                   'pendiente_contabilizar',
                   'Gastos CJ74 - Pendiente por Contabilizar'),
                   ('contabilizado', 'Gastos CJ74 - Contabilizado'), ])