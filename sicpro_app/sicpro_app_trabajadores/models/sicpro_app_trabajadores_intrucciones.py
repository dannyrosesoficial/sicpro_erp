# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models


class TrabajadoresIntrucciones(models.Model):
    _name = 'sicpro.app.trabajadores.intrucciones'
    _description = 'Instrucciones de los trabajadores'
    _order = "fecha_desde asc"

    plaza_id = fields.Char(string="# Plaza", required=True)
    name = fields.Many2one('sicpro.app.trabajadores', required=False, )
    instructor_plaza = fields.Char(string="Plaza Instructor", required=False)
    instructor = fields.Many2one('sicpro.app.trabajadores',
                                 string="Instructor", required=False, )
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                   'Puesto de trabajo',
                                   related='instructor.ocupacion_id')
    tipo_intruccion = fields.Char(string='Tipo de Instrucción', required=False)
    fecha_desde = fields.Date(string='Desde', required=False)
    evalucion = fields.Integer(string='Evaluación', required=False)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TrabajadoresIntrucciones, self).create(vals_list)
        for res in records:
            trabajador = self.env['sicpro.app.trabajadores'].search(
                [('plaza_id', '=', vals.get('plaza_id')), ])
            instructor = self.env['sicpro.app.trabajadores'].search(
                [('plaza_id', '=', vals.get('instructor_plaza')), ])
            res.name = trabajador.id
            res.instructor = instructor.id
            return res
        return None
