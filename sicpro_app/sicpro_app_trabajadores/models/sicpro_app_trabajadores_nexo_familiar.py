# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import models, fields


class TrabajadoresNexoFamiliar(models.Model):
    _name = 'sicpro.app.trabajadores.nexo.familiar'
    _description = 'Nexo Familiar del trabajador'

    trabajadores_id = fields.Many2one('sicpro.app.trabajadores',
                                      string="Trabajador")
    relacion_id = fields.Many2one('sicpro.app.trabajadores.familiar',
                                  string="Relación", required=True)
    nombre = fields.Many2one('sicpro.app.trabajadores', string='Nombre',
                             required=True)
    contacto = fields.Char(string='Contacto', related='nombre.movil_trabajo',
                           store=True)
    cumple = fields.Date(string="Cumpleaños",
                         related='nombre.fecha_nacimiento', store=True)
