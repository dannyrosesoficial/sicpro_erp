# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _


class DemandasCatalogo(models.Model):
    _name = "sicpro.app.demandas.catalogo"
    _description = 'Document'
    _order = 'id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Descripción SAP', required=True)
    codigo = fields.Char('Código', required=True)
    marca = fields.Char('Marca', required=True)
    especificaciones = fields.Text('Especificaciones', required=True)
    modelo = fields.Char('Modelo', required=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    company_currency = fields.Many2one("res.currency", string='Currency',
                                       related='company_id.currency_id',
                                       readonly=True)
    precio = fields.Monetary(
        currency_field='company_currency', string="Precio")
    tipo = fields.Char('Tipo', required=True)
    clasificacion = fields.Char('Clasificación', required=True)
    presupuesto = fields.Char('Presupuesto', required=True)
    active = fields.Boolean(string='Activo', default=True)
    etiquetas = fields.Many2many('sicpro.app.demandas.etiquetas',
                                 'sicpro_app_demandas_etiquetas_rel',
                                 string='Etiqueta')
    # Todos los campos de imagen están codificados en base64 y
    # son compatibles con PIL
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    # campos redimensionados almacenados (como archivo adjunto)para rendimiento
    image_1024 = fields.Image("Image 1024", related="image_1920",
                              max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512,
                             max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256,
                             max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128,
                             max_height=128, store=True)
    anio = fields.Char(string="Año", required=False,
                       default=fields.datetime.today().strftime("%Y"), )
