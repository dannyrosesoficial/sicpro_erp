# -*- coding: utf-8 -*-


from odoo import models, fields


class TrabajadoresNexoFamiliar(models.Model):
    _name = 'sicpro.app.trabajadores.nexo.familiar'
    _description = 'Nexo Familiar del trabajador'

    trabajadores_id = fields.Many2one('sicpro.app.trabajadores', string="Trabajador", invisible=1)
    relacion_id = fields.Many2one('sicpro.app.trabajadores.familiar', string="Relación", required="True")
    nombre = fields.Many2one('sicpro.app.trabajadores', string='Nombre', required="True")
    contacto = fields.Char(string='Contacto', related='nombre.movil_trabajo', store=True)
    cumple = fields.Date(string="Cumpleaños", related='nombre.fecha_nacimiento', store=True)
