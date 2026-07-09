# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date
from random import randint


class ViveresTrabajadoresEntregas(models.Model):
    _name = 'sicpro.app.viveres.trabajadores.entregas'
    _description = "Entregas a los trabajadores, módulo de víveres"

    name = fields.Many2one('sicpro.app.viveres.areas', string='Área', )
    jefe_area = fields.Many2one('sicpro.app.trabajadores', string='Responsable', related='name.name.manager_id',
                                store=True, )
    active = fields.Boolean('Activo', default=True)
    trabajador_id = fields.Many2one('sicpro.app.trabajadores', string='Trabajador', )
    producto_comprado_trabajador = fields.Many2many('sicpro.app.viveres.productos.comprados',
                                                    'sicpro_app_trabajador_entregas_rel', 'trabajador_entrega_id',
                                                    'producto_comprado_trabajador_id', string='Producto')
    fecha_entrega = fields.Date('Fecha entrega al área', compute='_compute_fecha_entrega_area', readonly=True)
    fecha_entrega_trabajador = fields.Date('Fecha entrega al trabajador')
    observaciones = fields.Text(string="Observaciones", required=False, )
    estado = fields.Selection(string="Estado", default='pendiente',
                              selection=[('entregado', 'Entregado'), ('no_entregado', 'No entregado'),
                                         ('pendiente', 'Pendiente de entrega')])

    @api.depends('producto_comprado_trabajador.producto_id', 'name.name')
    def _compute_fecha_entrega_area(self):
        for each in self:
            entrega_area = self.env['sicpro.app.viveres.areas.entregas'].search(
                ['&', ('name', '=', each.name.id), ('producto_comprado', 'in', self.producto_comprado_trabajador.ids)])

            if entrega_area:
                each.fecha_entrega = entrega_area.fecha
            else:
                each.fecha_entrega = None

    @api.depends('fecha_entrega_trabajador')
    def _compute_estado(self):
        if self.fecha_entrega_trabajador:
            self.estado = 'entregado'

    @api.constrains('estado')
    def restriccion_estado_pendiente(self):
        if self.estado == 'pendiente':
            if not self.observaciones:
                raise UserError(
                    'Debe especificar en las observaciones por qué queda pendiente la entrega al trabajador,'
                    ' verifíquelo. Si cree que es un error contacte al administrador')

    @api.constrains('fecha_entrega_trabajador')
    def restriccion_fecha_entrega_trabajador(self):
        if self.fecha_entrega_trabajador:
            today = date.today()
            if self.fecha_entrega_trabajador > today:
                raise UserError('La fecha de entrega al trabajador no puede ser superior al día de hoy,'
                                ' verifíquelo. Si cree que es un error contacte al administrador')
            elif self.fecha_entrega:
                if self.fecha_entrega_trabajador < self.fecha_entrega:
                    raise UserError(
                        'La fecha de entrega al trabajador no puede ser inferior a la fecha de entrega al área,'
                        ' verifíquelo. Si cree que es un error contacte al administrador')
