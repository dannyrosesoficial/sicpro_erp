# -*- coding: utf-8 -*-

from odoo import models, fields


class ViveresAreasEntregasResumenes(models.Model):
    _name = 'sicpro.app.viveres.areas.entregas.resumenes'
    _description = "Resumen entregas por áreas, módulo de víveres"

    name = fields.Many2one('sicpro.app.viveres.areas', string='Área', )
    direccion = fields.Many2one('res.company', string='Dirección', related='name.direccion', store=True, )
    active = fields.Boolean('Activo', default=True)
    producto = fields.Many2one('sicpro.app.viveres.productos.comprados', string='Producto', )
    fecha_compra = fields.Date('Fecha de compra', related='producto.fecha', store=True)
    fecha_entrega = fields.Date('Fecha de entrega al área', compute='_compute_fecha_entrega_area', readonly=True)
    total_entregado_area = fields.Integer('Total entregado al área', compute='_compute_total_entregado_area',
                                          readonly=True)
    total_entregado_trabajadores = fields.Integer('Total de trabajdores beneficiados',
                                                  compute='_compute_total_entregado_trabajadores_area', readonly=True)
    total_pendiente = fields.Integer('Total pendientes', compute='_compute_total_pendiente_trabajadores_area',
                                     readonly=True)
    total_no_entregado = fields.Integer('Total no entregados', compute='_compute_total_no_entregado_trabajadores_area',
                                        readonly=True)

    def _compute_fecha_entrega_area(self):
        for each in self:
            entrega_area = self.env['sicpro.app.viveres.areas.entregas'].search([('name', '=', each.name.id)])
            if entrega_area:
                for producto in entrega_area.producto_comprado:
                    if producto:
                        each.fecha_entrega = entrega_area.fecha

    def _compute_total_entregado_area(self):
        for each in self:
            entrega_area = self.env['sicpro.app.viveres.areas.entregas'].search([('name', '=', each.name.id)])
            if entrega_area:
                for producto in entrega_area.producto_comprado:
                    if producto:
                        each.total_entregado_area = entrega_area.total_entregado

    def _compute_total_entregado_trabajadores_area(self):
        for each in self:
            entrega_trabajador_area = self.env['sicpro.app.viveres.trabajadores.entregas'].search(
                ['&', ('name', '=', each.name.id), ('estado', '=', 'entregado')])
            if entrega_trabajador_area:
                for entrega in entrega_trabajador_area:
                    if entrega:
                        for producto in entrega.producto_comprado_trabajador:
                            if producto.id == each.producto.id:
                                each.total_entregado_trabajadores += 1
                            else:
                                each.total_entregado_trabajadores += 0
            else:
                each.total_entregado_trabajadores = 0

    def _compute_total_pendiente_trabajadores_area(self):
        for each in self:
            entrega_trabajador_area = self.env['sicpro.app.viveres.trabajadores.entregas'].search(
                ['&', ('name', '=', each.name.id), ('estado', '=', 'pendiente')])
            if entrega_trabajador_area:
                for entrega in entrega_trabajador_area:
                    if entrega:
                        for producto in entrega.producto_comprado_trabajador:
                            if producto.id == each.producto.id:
                                each.total_pendiente += 1
                            else:
                                each.total_pendiente += 0
            else:
                each.total_pendiente = 0

    def _compute_total_no_entregado_trabajadores_area(self):
        for each in self:
            entrega_area = self.env['sicpro.app.viveres.areas.entregas'].search(
                ['&', ('producto_comprado', '=', each.producto.id), ('name', '=', each.name.id)])
            if entrega_area:
                each.total_no_entregado = entrega_area.total_no_entregado
            else:
                each.total_no_entregado = 0
