# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PreparacionTecnicaMateriales(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.materiales'
    _description = 'Materiales de la Preparación Técnica'

    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=True, )
    product_id = fields.Many2one(
        comodel_name="sicpro.app.materiales.insumos", string="Material",
        required=True, domain=[('tipo', '=', 'material')], )
    cantidad = fields.Integer(string="Cantidad", required=True)
    codigo = fields.Char(string="Código de producto",
                         compute='_compute_codigo', compute_sudo=True,
                         store=True, )
    um = fields.Many2one(comodel_name="sicpro.app.materiales.insumos.um",
                         string="UMB", compute='_compute_um',
                         compute_sudo=True, store=True, )
    precio = fields.Float(string="Precio", compute='_compute_precio',
                          compute_sudo=True, store=True, )
    fecha_actualizado_sap = fields.Date('Actualización SAP',
                                        compute='_compute_fecha_actualizado_sap',
                                        compute_sudo=True, store=True, )
    fecha_importado = fields.Date('Fecha de Importación',
                                  compute='_compute_fecha_importado',
                                  compute_sudo=True, store=True, )
    tag_ids = fields.Many2many('sicpro.app.materiales.insumos.etiquetas',
                               'sicpro_app_materiales_preparaciones_etiquetas_rel',
                               'producto_id', 'tag_id', string='Etiqueta',
                               compute='_compute_tag_ids', compute_sudo=True,
                               store=True, )
    ce = fields.Char(string="Ce", compute='_compute_ce', compute_sudo=True,
                     store=True, )
    company_id = fields.Many2one('res.company', string='Proceso', required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    presupuesto = fields.Monetary("Presupuesto",
                                  compute='_compute_presupuesto',
                                  compute_sudo=True, store=True,
                                  currency_field='company_currency_id')

    # devuelve el valor del codigo
    @api.depends('product_id')
    def _compute_codigo(self):
        for data in self:
            data.codigo = data.product_id.material_insumo

    # devuelve el valor del um
    @api.depends('product_id')
    def _compute_um(self):
        for data in self:
            data.um = data.product_id.um

    # devuelve el valor del precio
    @api.depends('product_id')
    def _compute_precio(self):
        for data in self:
            data.precio = data.product_id.precio

    # devuelve el valor de la fecha de actualización sap
    @api.depends('product_id')
    def _compute_fecha_actualizado_sap(self):
        for data in self:
            data.fecha_actualizado_sap = data.product_id.fecha_actualizado_sap

    # devuelve el valor de la fecha de importado
    @api.depends('product_id')
    def _compute_fecha_importado(self):
        for data in self:
            data.fecha_importado = data.product_id.fecha_importado

    # devuelve el valor del ce
    @api.depends('product_id')
    def _compute_ce(self):
        for data in self:
            data.ce = data.product_id.ce

    # devuelve el valor de la etiqueta
    @api.depends('product_id')
    def _compute_tag_ids(self):
        for data in self:
            data.tag_ids = data.product_id.tag_ids

    # calculo el valor del presupuesto
    @api.depends('cantidad', 'precio')
    def _compute_presupuesto(self):
        for data in self:
            data.presupuesto = data.cantidad * data.precio

    @api.constrains("cantidad")
    def _check_quantity(self):
        for material in self:
            if not material.cantidad > 0.0:
                raise ValidationError(
                    _("Quantity of material consumed must be greater than 0.")
                )


class PreparacionTecnicaInsumos(models.Model):
    _name = 'sicpro.app.preparacion.tecnica.insumos'
    _description = 'Insumos de la Preparación Técnica'

    preparaciones_id = fields.Many2one(
        comodel_name="sicpro.app.preparacion.tecnica.preparaciones",
        string="Preparaciones", ondelete="cascade", required=True, )
    product_id = fields.Many2one(
        comodel_name="sicpro.app.materiales.insumos", string="Material",
        required=True, domain=[('tipo', '=', 'insumo')], )
    cantidad = fields.Integer(string="Cantidad", required=True)
    codigo = fields.Char(string="Código de producto",
                         compute='_compute_codigo', compute_sudo=True,
                         store=True, )
    um = fields.Many2one(comodel_name="sicpro.app.materiales.insumos.um",
                         string="UMB", compute='_compute_um',
                         compute_sudo=True, store=True, )
    precio = fields.Float(string="Precio", compute='_compute_precio',
                          compute_sudo=True, store=True, )
    fecha_actualizado_sap = fields.Date('Actualización SAP',
                                        compute='_compute_fecha_actualizado_sap',
                                        compute_sudo=True, store=True, )
    fecha_importado = fields.Date('Fecha de Importación',
                                  compute='_compute_fecha_importado',
                                  compute_sudo=True, store=True, )
    tag_ids = fields.Many2many('sicpro.app.materiales.insumos.etiquetas',
                               'sicpro_app_insumos_preparaciones_etiquetas_rel',
                               'producto_id', 'tag_id', string='Etiqueta',
                               compute='_compute_tag_ids', compute_sudo=True,
                               store=True, )
    ce = fields.Char(string="Ce", compute='_compute_ce', compute_sudo=True,
                     store=True, )
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency_id = fields.Many2one('res.currency', string="Currency",
                                          related='company_id.currency_id',
                                          readonly=True)
    presupuesto = fields.Monetary("Presupuesto",
                                  compute='_compute_presupuesto',
                                  compute_sudo=True, store=True,
                                  currency_field='company_currency_id')

    # devuelve el valor del codigo
    @api.depends('product_id')
    def _compute_codigo(self):
        for data in self:
            data.codigo = data.product_id.material_insumo

    # devuelve el valor del um
    @api.depends('product_id')
    def _compute_um(self):
        for data in self:
            data.um = data.product_id.um

    # devuelve el valor del precio
    @api.depends('product_id')
    def _compute_precio(self):
        for data in self:
            data.precio = data.product_id.precio

    # devuelve el valor de la fecha de actualización sap
    @api.depends('product_id')
    def _compute_fecha_actualizado_sap(self):
        for data in self:
            data.fecha_actualizado_sap = data.product_id.fecha_actualizado_sap

    # devuelve el valor de la fecha de importado
    @api.depends('product_id')
    def _compute_fecha_importado(self):
        for data in self:
            data.fecha_importado = data.product_id.fecha_importado

    # devuelve el valor del ce
    @api.depends('product_id')
    def _compute_ce(self):
        for data in self:
            data.ce = data.product_id.ce

    # devuelve el valor de la etiqueta
    @api.depends('product_id')
    def _compute_tag_ids(self):
        for data in self:
            data.tag_ids = data.product_id.tag_ids

    # calculo el valor del presupuesto
    @api.depends('cantidad', 'precio')
    def _compute_presupuesto(self):
        for data in self:
            data.presupuesto = data.cantidad * data.precio

    @api.constrains("cantidad")
    def _check_quantity(self):
        for material in self:
            if not material.cantidad > 0.0:
                raise ValidationError(
                    _("Quantity of insumo consumed must be greater than 0.")
                )
