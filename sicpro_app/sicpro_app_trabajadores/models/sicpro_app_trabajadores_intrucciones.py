# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import models, fields, api

class TrabajadoresIntrucciones(models.Model):
    _name = 'sicpro.app.trabajadores.intrucciones'
    _description = 'Instrucciones de los trabajadores'
    _order = "fecha_desde asc"

    plaza_id = fields.Char(string="# Plaza", required=True)

    name = fields.Many2one(
        'sicpro.app.trabajadores',
        string='Trabajador',
        compute='_compute_trabajadores',
        store=True,
        readonly=False,
    )

    instructor_plaza = fields.Char(string="Plaza Instructor")

    instructor = fields.Many2one(
        'sicpro.app.trabajadores',
        string="Instructor",
        compute='_compute_trabajadores',
        store=True,
        readonly=False,
    )

    ocupacion_id = fields.Many2one(
        'sicpro.app.trabajadores.ocupacion',
        'Puesto de trabajo',
        related='instructor.ocupacion_id',
    )

    tipo_intruccion = fields.Char(string='Tipo de Instrucción')
    fecha_desde = fields.Date(string='Desde')
    evalucion = fields.Integer(string='Evaluación')

    @api.depends('plaza_id', 'instructor_plaza')
    def _compute_trabajadores(self):
        Trabajador = self.env['sicpro.app.trabajadores']
        for rec in self:
            rec.name = (
                Trabajador.search([('plaza_id', '=', rec.plaza_id)], limit=1)
                if rec.plaza_id else False
            )
            rec.instructor = (
                Trabajador.search([('plaza_id', '=', rec.instructor_plaza)], limit=1)
                if rec.instructor_plaza else False
            )
