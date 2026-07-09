# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import fields, models, api


class CalendarPlanReport(models.Model):
    _name = 'calendar.tareas.principales.generales'
    _description = 'Registros de tareas principales y generales'
    _order = 'anio desc, codigo_mes desc, tipo desc'

    tipo = fields.Selection([('principales', 'Tareas Principales'),
                             ('generales', 'Tareas Generales')], required=True,
                            string="Tipo")
    name = fields.Char(string='Tarea', required=True)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses',
                          string='Mes', required=True)
    codigo_mes = fields.Integer(string="Código Mes", required=True)
    anio = fields.Char(string='Año', required=True,
                       default=fields.Datetime.now().strftime("%Y"))
    active = fields.Boolean(string="Activo", default=True, index=True)

    @api.onchange('mes')
    def onchange_mes(self):
        for item in self:
            if item.mes:
                item.codigo_mes = item.mes.codigo_mes
            else:
                item.codigo_mes = None
