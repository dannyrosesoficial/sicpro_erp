# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import fields, models


class MaterialesInsumos(models.Model):
    _name = "sicpro.app.materiales.insumos"
    _description = "Materiales e insumos"
    _order = "id asc"
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Nombre", required=True, index=True)
    ce = fields.Char(string="Ce", required=True)
    material_insumo = fields.Char(string="Código de producto", required=True)
    um = fields.Many2one(comodel_name="sicpro.app.materiales.insumos.um",
                         string="UMB", required=True)
    precio = fields.Float(string="Precio", required=True)
    fecha_actualizado_sap = fields.Date(string='Actualización SAP', required=True)
    fecha_importado = fields.Date(string='Fecha de Importación', readonly=True,
                                  default=fields.Datetime.now,
                                  help="Fecha en que se actualiza el producto")
    tag_ids = fields.Many2many('sicpro.app.materiales.insumos.etiquetas',
                               'sicpro_app_materiales_insumos_etiquetas_rel',
                               'producto_id', 'tag_id', string='Etiqueta',
                               help="Clasifica los materiales e insumos")

    tipo = fields.Selection([('material', 'Material'), ('insumo', 'Insumo')],
                            index=True, required=True,
                            tracking=15, help="tipo de producto")
    notas = fields.Char(string="Notas", required=False)
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920",
                             max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920",
                             max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920",
                             max_width=128, max_height=128, store=True)
    active = fields.Boolean(string='Activo', default=True, tracking=True, index=True)
    color = fields.Integer(string='Indices de colores', default=0)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id)
    image_tipo = fields.Image("imagen tipo", max_width=128, max_height=128,
                              store=True)
