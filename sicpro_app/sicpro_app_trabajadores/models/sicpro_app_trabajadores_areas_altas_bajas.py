# -*- coding: utf-8 -*-

from odoo import models, fields


class TrabajadoresAreasAltasBajas(models.Model):
    _name = 'sicpro.app.trabajadores.areas.altas.bajas'
    _description = "Altas y bajas mensuales por áreas, módulo de trabajadores"

    name = fields.Many2one('sicpro.app.trabajadores.areas', string='Área', )
    direccion = fields.Many2one('res.company', string='Proceso', related='name.company_id', store=True, )
    active = fields.Boolean('Activo', default=True)
    mes = fields.Many2one(comodel_name='sicpro.nomenclador.meses', string='Mes', required=True)
    codigo_mes = fields.Integer(string="Código Mes", related='mes.codigo_mes')
    anio = fields.Char(string='Año', required=True, default=fields.Datetime.now().strftime("%Y"))
    trabajador = fields.Many2one('sicpro.app.trabajadores', 'Trabajador')
    estado = fields.Selection(selection=[('alta', 'Alta'), ('baja', 'Baja')], string='Estado', )
    fecha = fields.Date('Fecha')
