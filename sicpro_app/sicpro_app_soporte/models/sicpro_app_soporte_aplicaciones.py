# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import base64
import os
from odoo import api, models, fields


class SoporteAplicaciones(models.Model):
    _name = 'sicpro.app.soporte.aplicaciones'
    _description = 'Soporte de aplicaciones del sistema'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_image(self):
        # Localizamos la carpeta del modelo actual
        current_path = os.path.dirname(__file__)
        image_path = os.path.join(current_path, '..', 'static', 'src', 'img',
                                  'modulo.png')
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read())
        return False

    def _get_default_stage_id(self):
        return self.env['sicpro.app.soporte.estados.aplicaciones'].search([],
                                                                          limit=1).id

    name = fields.Char(string='Aplicación', required=True)
    active = fields.Boolean(string='Activo', default=True, index=True)
    stage_id = fields.Many2one('sicpro.app.soporte.estados.aplicaciones',
                               string='Estado',
                               group_expand='_read_group_stage_ids',
                               default=_get_default_stage_id,
                               tracking=True)  # Agregado tracking para SICPRO

    estado_desarrollo = fields.Boolean(string='Estado Desarrollo',
                                       related='stage_id.desarrollo')
    descripcion = fields.Text(string="Descripción", required=False)
    fecha_desarrollo = fields.Date(string='En Desarrollo', required=False)
    fecha_produccion = fields.Date(string='En Producción', required=False)
    fecha_detenido = fields.Date(string='Detenido', required=False)
    fecha_descontinuado = fields.Date(string='Descontinuado', required=False)

    tipo = fields.Selection(string='Tipo', selection=[('modulo', 'Módulo'),
        ('aplicacion', 'Aplicación')], required=False, default='modulo')

    # --- SECCIÓN DE IMÁGENES CORREGIDA PARA ODOO 19 ---
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920,
                              default=_default_image)

    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True,
                              readonly=False)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True, readonly=False)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True, readonly=False)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True, readonly=False)
    # --------------------------------------------------

    modulo_base = fields.Boolean(string='Módulo Base', required=False)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        stage_ids = self.env['sicpro.app.soporte.estados.aplicaciones'].search(
            [])
        return stage_ids

    def write(self, vals):
        # Ejecutamos el super primero para tener los datos actualizados
        res = super(SoporteAplicaciones, self).write(vals)

        if 'stage_id' in vals:
            now = fields.Date.context_today(self)
            for item in self:
                stage = item.stage_id
                if stage.desarrollo:
                    item.fecha_desarrollo = now
                elif stage.detenido:
                    item.fecha_detenido = now
                elif stage.closed:
                    item.fecha_produccion = now
                elif stage.descontinuado:
                    item.fecha_descontinuado = now
        return res