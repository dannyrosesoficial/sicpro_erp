# -*- coding: utf-8 -*-

from random import randint
from odoo import models, fields, api
from odoo.exceptions import UserError


def _default_color():
    return randint(1, 11)


class ViveresProductosComprados(models.Model):
    _name = 'sicpro.app.viveres.productos.comprados'
    _description = "Módulo de víveres, productos comprados para la distribución"
    _rec_name = 'producto_id'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _order = "id desc"

    # Es necesario para la inicialización la incorporación del campo id
    id = fields.Id()

    producto_id = fields.Many2one('sicpro.app.viveres.productos', string='Producto', required=True)
    name = fields.Char(string='Nombre', related='producto_id.name', required=False)
    numero = fields.Integer('Número', required=True)
    # Todos los campos de imagen están codificados en base64 y son compatibles con PIL
    image_1920 = fields.Image("Image", related='producto_id.image_1920', max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    fecha = fields.Date('Fecha de compra', required=True)
    precio = fields.Monetary('Precio', currency_field='company_currency', required=True)
    active = fields.Boolean('Activo', default=True)
    estado = fields.Selection(string="Estado", default='pendiente', compute="_compute_is_completed",
                              selection=[('entregado', 'Entregado'), ('pendiente', 'Pendiente de entrega')])
    color = fields.Integer(string='Color', default=lambda self: _default_color())
    is_check = fields.Boolean("Check", compute="_compute_is_check", default=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)
    company_currency = fields.Many2one(string='Currency', readonly=True, related='company_id.currency_id')

    def _compute_is_check(self):
        areas = self.env['sicpro.app.viveres.areas'].search([('active', '=', True)])
        for each in self:
            entrega_completa = True
            for area in areas:
                area_producto_entregado = self.env['sicpro.app.viveres.areas.entregas'].search(
                    ['&', ('name', '=', area.id), ('producto_comprado', '=', each.id), ('active', '=', True)])
                if not area_producto_entregado:
                    entrega_completa = False
            if entrega_completa:
                each.sudo().write({'estado': 'entregado'})
            else:
                each.sudo().write({'estado': 'pendiente'})
            each.is_check = entrega_completa

    def _compute_is_completed(self):
        areas = self.env['sicpro.app.viveres.areas'].search([('active', '=', True)])
        for each in self:
            entrega_completa = True
            for area in areas:
                area_producto_entregado = self.env['sicpro.app.viveres.areas.entregas'].search(
                    ['&', ('name', '=', area.id), ('producto_comprado', '=', each.id), ('active', '=', True)])
                if not area_producto_entregado:
                    entrega_completa = False
            if entrega_completa:
                each.estado = 'entregado'
            else:
                each.estado = 'pendiente'

    @api.model
    def create(self, vals):
        res = super(ViveresProductosComprados, self).create(vals)

        porductos_comprados = self.env['sicpro.app.viveres.productos.comprados'].search(
            ['&', ('producto_id', '=', res['producto_id'].name), ('estado', '=', 'pendiente'), ('id', '!=', res['id'])])
        if porductos_comprados:
            raise UserError('Existe productos de este tipo aún sin entregar a las áreas,'
                            ' verifíquelo. Si cree que es un error contacte al administrador')
        return res
