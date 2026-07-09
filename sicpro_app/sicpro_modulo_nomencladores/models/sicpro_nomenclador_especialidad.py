# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NomencladorEspecialidad(models.Model):
    _name = 'sicpro.nomenclador.especialidad'
    _description = 'Especialidades de ejecución'

    name = fields.Char(required=True, string='Especialidad')
    codigo = fields.Integer(string="Código", required=True, )
    letra = fields.Char(string="Letra", required=True, )
    company_id = fields.Many2one(comodel_name="res.company",
                                 string="Proceso", required=True, )
    active = fields.Boolean(string="Activo", default=True, )
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
