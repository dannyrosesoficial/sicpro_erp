# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields, api


class SoporteVeriones(models.Model):
    _name = 'sicpro.app.soporte.versiones'
    _description = 'Soporte de versiones del sistema'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados.versiones'].search([],
                                                                       limit=1).id

    name = fields.Char(string='Versión', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    stage_id = fields.Many2one('sicpro.app.soporte.estados.versiones',
                               string='Estado',
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id)
    estado_final = fields.Boolean(string='Estado Final',
                                  related='stage_id.closed')
    paquetes_ids = fields.One2many(comodel_name='sicpro.app.soporte.paquetes',
                                   inverse_name='version_id',
                                   string='Paquetes Linux')
    aplicaciones_ids = fields.Many2many(
        comodel_name='sicpro.app.soporte.aplicaciones',
        relation='sicpro_app_soporte_versiones_aplicacion_rel',
        string='Aplicaciones', domain="[('estado_desarrollo','=',True)]")
    tickets_ids = fields.One2many(comodel_name='sicpro.app.soporte',
                                  inverse_name='version_id',
                                  string='Ticket de Soporte')
    cuenta_paquetes = fields.Integer(string='Cantidad de Paquetes',
                                     required=False,
                                     compute='_compute_aplicaciones')
    cuenta_aplicaciones = fields.Integer(string='Cantidad de Aplicaciones',
                                         required=False,
                                         compute='_compute_aplicaciones')
    cuenta_actividades = fields.Integer(string='Cantidad de Actividades',
                                        required=False,
                                        compute='_compute_aplicaciones')

    # Cuenta los paquetes, aplicaciones y actividades de la versión
    @api.depends('paquetes_ids', 'aplicaciones_ids', 'tickets_ids')
    def _compute_aplicaciones(self):
        for record in self:
            record.cuenta_paquetes = len(record.paquetes_ids)
            record.cuenta_aplicaciones = len(record.aplicaciones_ids)
            record.cuenta_actividades = len(record.tickets_ids)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        stage_ids = self.env['sicpro.app.soporte.estados.versiones'].search([])
        return stage_ids
