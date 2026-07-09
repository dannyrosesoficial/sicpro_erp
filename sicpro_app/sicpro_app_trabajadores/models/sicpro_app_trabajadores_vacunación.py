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
    name = fields.Many2one('sicpro.app.trabajadores', required=False, )
    tipo_vacuna = fields.Char(string='Tipo de Vacuna', required=False)
    fecha = fields.Date(string='Fecha', required=False)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TrabajadoresVacunacion, self).create(vals_list)
        for res in records:
            trabajador = self.env['sicpro.app.trabajadores'].search(
                [('plaza_id', '=', vals.get('plaza_id')), ])
            res.name = trabajador.id
            return res
        return None
