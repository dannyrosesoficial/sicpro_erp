# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class SoporteEstados(models.Model):
    _name = 'sicpro.app.soporte.estados'
    _description = 'Estados del Soporte'
    _order = 'sequence, id'

    name = fields.Char(string='Estado', required=True)
    descripcion = fields.Text(string='Descripción')
    sequence = fields.Integer(string='Secuencia', default=1, index=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    inicial = fields.Boolean(string='Estado inicial')
    pendiente_correo_acceso = fields.Boolean(string='Pendiente Correo Acceso')
    unattended = fields.Boolean(string='No Procede')
    closed = fields.Boolean(string='Estado final')
    mail_template_id = fields.Many2one('mail.template',
                                       string='Email Template', domain=[
            ('model', '=', 'sicpro.app.soporte')], )
    fold = fields.Boolean(string='Solapado en Kanban')
    company_id = fields.Many2one('res.company', string="Proceso",
                                 default=lambda self: self.env.company)
