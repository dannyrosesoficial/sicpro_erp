# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models


class TrabajadoresVacunacion(models.Model):
    _name = 'sicpro.app.trabajadores.vacunacion'
    _description = 'Vacunación de los trabajadores'
    _order = "fecha asc"

    plaza_id = fields.Char(string="# Plaza", required=True)
    tipo_vacuna = fields.Char(string='Tipo de Vacuna', required=False)
    fecha = fields.Date(string='Fecha', required=False)
    name = fields.Many2one('sicpro.app.trabajadores', string='Trabajador',
        compute='_compute_name', store=True, readonly=False, )

    @api.depends('plaza_id')
    def _compute_name(self):
        for rec in self:
            if rec.plaza_id:
                trabajador = self.env['sicpro.app.trabajadores'].search(
                    [('plaza_id', '=', rec.plaza_id)], limit=1)
                rec.name = trabajador.id if trabajador else False
            else:
                rec.name = False

