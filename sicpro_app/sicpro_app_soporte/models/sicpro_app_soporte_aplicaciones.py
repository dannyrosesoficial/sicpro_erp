# -*- coding: utf-8 -*-

import base64

from odoo import api
from odoo import models, fields
from odoo.modules.module import get_module_resource


class SoporteAplicaciones(models.Model):
    _name = 'sicpro.app.soporte.aplicaciones'
    _description = 'Soporte de aplicaciones del sistema'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_image(self):
        image_path = get_module_resource('sicpro_app_soporte', 'static/src/img', 'modulo.png')
        return base64.b64encode(open(image_path, 'rb').read())

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados.aplicaciones'].search(
            [], limit=1).id

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string='Aplicación', required=True)
    active = fields.Boolean(default=True)
    stage_id = fields.Many2one('sicpro.app.soporte.estados.aplicaciones', string='Estado',
                               group_expand='_read_group_stage_ids', default=_get_default_stage_id,)
    estado_desarrollo = fields.Boolean(string='Estado Desarrollo', related='stage_id.desarrollo')
    descripcion = fields.Text(string="Descripción", required=False)
    fecha_desarrollo = fields.Date(string='En Desarrollo', required=False)
    fecha_produccion = fields.Date(string='En Producción', required=False)
    fecha_detenido = fields.Date(string='Detenido', required=False)
    fecha_descontinuado = fields.Date(string='Descontinuado', required=False)
    tipo = fields.Selection(string='Tipo', selection=[('modulo', 'Módulo'), ('aplicacion', 'Aplicación'), ],
                            required=False, )
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920, default=_default_image)
    # campos redimensionados almacenados (como adjunto) para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')
    modulo_base = fields.Boolean(string='Módulo Base', required=False)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['sicpro.app.soporte.estados.aplicaciones'].search([])
        return stage_ids

    def write(self, vals):
        res = super(SoporteAplicaciones, self).write(vals)
        for item in self:
            now = fields.Datetime.now()
            if vals.get('stage_id'):
                stage_obj = self.env['sicpro.app.soporte.estados.aplicaciones'].browse([vals['stage_id']])
                if stage_obj.desarrollo:
                    item['fecha_desarrollo'] = now
                if stage_obj.detenido:
                    item['fecha_detenido'] = now
                if stage_obj.closed:
                    item['fecha_produccion'] = now
                if stage_obj.descontinuado:
                    item['fecha_descontinuado'] = now


        return res



