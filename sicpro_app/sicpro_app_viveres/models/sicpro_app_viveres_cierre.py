# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields


class ViveresCierre(models.Model):
    _name = 'sicpro.app.viveres.cierre'
    _description = "Cierres mensuales de Capital Humano para módulo víveres"
    _order = "codigo_mes desc, name asc"
    _inherit = ['mail.thread']

    def _areas_ids(self):
        areas = self.env['sicpro.app.trabajadores.areas'].search(
            [('active', '=', True)])
        if areas:
            return areas

    name = fields.Many2one('sicpro.app.viveres.areas', string='Área',
                           default=_areas_ids, )
    direccion = fields.Many2one('res.company', string='Dirección',
                                related='name.direccion', store=True, )
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', )
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes')
    anio = fields.Char(string='Año',
                       default=fields.Datetime.now().strftime("%Y"))
    total = fields.Integer(string='Total de trabajadores', )
    altas = fields.Integer(string='Cantidad de altas', )
    bajas = fields.Integer(string='Cantidad de bajas', )
    active = fields.Boolean(string='Activo', default=True, index=True)
    estado = fields.Selection(selection=[('ok', 'OK'), ('error', 'Error')],
                              string='Estado', default='ok')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
