# -*- coding: utf-8 -*-

from odoo import api, fields, models


class TrabajadoresVacunacion(models.Model):
    _name = 'sicpro.app.trabajadores.vacunacion'
    _description = 'Vacunación de los trabajadores'
    _order = "fecha asc"

    plaza_id = fields.Char(string="# Plaza", required=True)
    name = fields.Many2one('sicpro.app.trabajadores', required=False,)
    tipo_vacuna = fields.Char(string='Tipo de Vacuna', required=False)
    fecha = fields.Date(string='Fecha', required=False)

    @api.model
    def create(self, vals):
        vacunacion = super(TrabajadoresVacunacion, self).create(vals)
        trabajador = self.env['sicpro.app.trabajadores'].search(
            [('plaza_id', '=', vals.get('plaza_id')), ])
        vacunacion['name'] = trabajador.id
        return vacunacion
