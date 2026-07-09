# -*- coding: utf-8 -*-

from odoo import fields, models


class MaterialesInsumos(models.Model):
    _name = "sicpro.app.materiales.insumos"
    _description = "Materiales e insumos"
    _order = "id asc"
    _inherit = ['mail.thread.cc', 'mail.thread', 'mail.activity.mixin']

    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo \
            as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.\
                NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string="Nombre", required=True, index=True)
    ce = fields.Char(string="Ce", required=True, )
    material_insumo = fields.Char(string="Código de producto", required=True, )
    um = fields.Many2one(comodel_name="sicpro.app.materiales.insumos.um",
                         string="UMB", required=True, )
    precio = fields.Float(string="Precio", required=True, )
    fecha_actualizado_sap = fields.Date('Actualización SAP', required=True, )
    fecha_importado = fields.Date('Fecha de Importación', readonly=True,
                                  default=fields.Datetime.now,
                                  help="Fecha en que se actualiza el producto")
    tag_ids = fields.Many2many('sicpro.app.materiales.insumos.etiquetas',
                               'sicpro_app_materiales_insumos_etiquetas_rel',
                               'producto_id', 'tag_id', string='Etiqueta',
                               help="Clasifica los materiales e insumos")

    tipo = fields.Selection([('material', 'Material'), ('insumo', 'Insumo')],
                            index=True, required=True,
                            tracking=15, default=lambda self: 'iniciativa',
                            help="tipo de producto")
    notas = fields.Char(string="Notas", required=False, )
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
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
    active = fields.Boolean('Activo', default=True, tracking=True)
    color = fields.Integer('Indices de colores', default=0)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id)
    image_tipo = fields.Image("imagen tipo", max_width=128, max_height=128,
                              store=True)
