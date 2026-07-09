# -*- coding: utf-8 -*-

from odoo import models, fields


class TrabajadoresNotificacionCierre(models.Model):
    _name = 'sicpro.app.trabajadores.notificacion.cierre'
    _description = "Trabajadores a los que se le notificará el cierre mensual"
    
    name = fields.Many2one('sicpro.app.trabajadores', string='Trabajadores', required=True,)
    correo_trabajo = fields.Char('Correo Trabajo', related='name.correo_trabajo', required=True)
    proceso = fields.Many2one('res.company', related='name.company_id')
    active = fields.Boolean('Activo', default=True)
