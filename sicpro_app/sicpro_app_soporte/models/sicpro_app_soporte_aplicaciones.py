# -*- coding: utf-8 -*-

import base64
from datetime import timedelta,date,datetime
from odoo.modules.module import get_module_resource
from odoo import api, fields, models, _
from pytz import timezone, UTC
from odoo.tools import format_time
from random import randint
import qrcode
from io import BytesIO
from odoo import models, fields, _
from odoo.exceptions import UserError


class SoporteAplicaciones(models.Model):

    _name = 'sicpro.app.soporte.aplicaciones'
    _description = 'Soporte de aplicaciones del sistema'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_image(self):
        image_path = get_module_resource('sicpro_app_soporte',
                                         'static/src/img', 'modulo.png')
        return base64.b64encode(open(image_path, 'rb').read())

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados.aplicaciones'].search(
            [], limit=1).id

    name = fields.Char(string='Aplicación', required=True)
    active = fields.Boolean(default=True)
    stage_id = fields.Many2one('sicpro.app.soporte.estados.aplicaciones',
                               string='Estado',
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id,)
    descripcion = fields.Text(string="Descripción", required=False)
    fecha_desarrollo = fields.Date(string='Fecha en Desarrollo',
                                   required=False)
    fecha_produccion = fields.Date(string='Fecha en Producción',
                                   required=False)
    fecha_detenido = fields.Date(string='Fecha Detenido', required=False)
    fecha_descontinuado = fields.Date(string='Fecha Descontinuado',
                                      required=False)
    tipo = fields.Selection(string='Tipo',
                            selection=[('modulo', 'Módulo'),
                                       ('aplicacion', 'Aplicación'), ],
                            required=False, )

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920,
                              default=_default_image)
    # campos redimensionados almacenados (como adjunto) para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)




    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = self.env['sicpro.app.soporte.estados.aplicaciones'].search([])
        return stage_ids



