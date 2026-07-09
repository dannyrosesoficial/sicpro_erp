# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta, datetime


class ViveresTrabajadoresEntregaWizard(models.TransientModel):
    _name = "sicpro.app.viveres.trabajadores.entrega.wizard"
    _description = "Entrega de productos a los trabajadores"

    @api.onchange('productos_entregar_compute')
    def _productos_ids(self):
        self.productos_entregar = self.productos_entregar_compute

    @api.depends("area.name")
    def _compute_productos_a_entregar(self):
        for each in self:
            if each:
                productos = []
                entregas_area = self.env['sicpro.app.viveres.areas.entregas'].search(
                    ['&', ('active', '=', True), ('total_no_entregado', '>', 0), ('name', '=', each.area.id)])
                for entrega in entregas_area:
                    if entrega:
                        for producto in entrega.producto_comprado:
                            if producto:
                                productos.append(producto.id)

                each.productos_entregar_compute = productos

    @api.onchange('trabajadores_compute')
    def _trabajadores_ids(self):
        self.trabajadores = self.trabajadores_compute

    @api.depends("area.name")
    def _compute_trabajadores_ids(self):
        for each in self:
            if each:
                if each.area:
                    trabajadores_area = []
                    trabajadores = []
                    if each.area.name.tipo_registro == 'sin_categoría':
                        trabajadores_area = self.env['sicpro.app.trabajadores'].search(
                            ['&', ('active', '=', True), ('area_id.id', '=', each.area.name.id)])
                    else:
                        trabajadores_area = self.env['sicpro.app.trabajadores'].search(
                            ['&', ('active', '=', True), '|', ('area_id.id', '=', each.area.name.id),
                             ('area_id.parent_id.id', '=', each.area.name.id)])
                    # raise UserError(len(self.productos_entregar_compute))
                    if trabajadores_area and len(self.productos_entregar_compute) > 0:
                        for trabajador in trabajadores_area:
                            entrega_trabajador = self.env['sicpro.app.viveres.trabajadores.entregas'].search(
                                ['&', ('producto_comprado_trabajador', 'in', self.productos_entregar.ids),
                                    ('trabajador_id.id', '=', trabajador.id)])
                            if not entrega_trabajador:
                                trabajadores.append(trabajador.id)
                    each.trabajadores_compute = trabajadores

                else:
                    each.trabajadores_compute = []

    productos_entregar_compute = fields.Many2many('sicpro.app.viveres.productos.comprados',
                                                  'productos_entregar_compute_trabajador_wizard_rel',
                                                  'productos_entregar_compute_id', 'wizard_compute_id',
                                                  string="Productos Compute", compute='_compute_productos_a_entregar', )
    productos_entregar = fields.Many2many('sicpro.app.viveres.productos.comprados',
                                          'productos_entregar_trabajador_wizard_rel', 'productos_entregar_id',
                                          'wizard_id', string="Productos", )
    trabajadores_compute = fields.Many2many('sicpro.app.trabajadores', 'trabajador_compute_wizard_rel',
                                            'trabajador_compute_id', 'wizard_compute_trabajador_id',
                                            string='Entregado a Compute', compute='_compute_trabajadores_ids', )
    trabajadores = fields.Many2many('sicpro.app.trabajadores', 'trabajador_wizard_rel', 'trabajador_id',
                                    'wizard_trabajador_id', string='Entregado a', )

    fecha_entrega = fields.Date('Fecha entrega', default=fields.Datetime.now())

    estado = fields.Selection(string="Estado", default='pendiente',
                              selection=[('entregado', 'Entregado'), ('no_entregado', 'No entregado'),
                                         ('pendiente', 'Pendiente de entrega')])
    area = fields.Many2one('sicpro.app.viveres.areas', required=True)

    observaciones = fields.Text(string="Observaciones", required=False, )

    def realizar_entrega(self):
        ok = True
        entregas_area = self.env['sicpro.app.viveres.areas.entregas'].search(
            ['&', ('active', '=', True), ('total_no_entregado', '>', 0), ('name', '=', self.area.id)])

        for entrega in entregas_area:
            if entrega:
                if entrega.total_no_entregado < len(self.trabajadores_compute):
                    ok = False
        # raise UserError(ok)
        if not ok:
            raise UserError('El listado de trabajadores es mayor a la cantidad de productos a entregar,'
                            ' verifíquelo. Si cree que es un error contacte al administrador')

        total_entregado = 0
        for trabajador in self.trabajadores:
            if trabajador:
                entrega_trabajador = self.env['sicpro.app.viveres.trabajadores.entregas'].search(
                    ['&', ('producto_comprado_trabajador', 'in', self.productos_entregar.ids),
                        ('trabajador_id.id', '=', trabajador.id)])

                if not entrega_trabajador:
                    self.env['sicpro.app.viveres.trabajadores.entregas'].sudo().create(
                        {'name': self.area.id, 'trabajador_id': trabajador.id,
                            'producto_comprado_trabajador': self.productos_entregar.ids,
                            'fecha_entrega_trabajador': self.fecha_entrega, 'estado': self.estado})
                    total_entregado += 1

        entrega_area = self.env['sicpro.app.viveres.areas.entregas'].search(
            ['&', ('producto_comprado', 'in', self.productos_entregar.ids), ('name', '=', self.area.id)])
        if entrega_area:
            total_entregado = entrega_area.total_no_entregado - total_entregado
            entrega_area.sudo().write({'total_no_entregado': total_entregado})

    @api.constrains('estado')
    def restriccion_estado(self):
        if self.estado:
            if self.estado == 'pendiente' or self.estado == 'no_entregado':
                if not self.observaciones:
                    raise UserError('Debe especificar en las observaciones el por qué no se entregó el producto,'
                                    ' verifíquelo. Si cree que es un error contacte al administrador')
