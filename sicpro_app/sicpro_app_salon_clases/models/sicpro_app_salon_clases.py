# -*- coding: utf-8 -*-

import logging
from datetime import timedelta, datetime

from odoo import fields, models, api, SUPERUSER_ID, _
from odoo.tools import format_date

_logger = logging.getLogger(__name__)

Prioridades_Activas = [('0', 'Baja'), ('1', 'Media'), ('2', 'Alta'),
                       ('3', 'Muy Alta'), ]


class SalonClases(models.Model):
    _name = 'sicpro.app.salon.clases'
    _description = 'Salón de Clases'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id asc"

    def _get_default_temas(self):
        self.temas_id = self.env.context.get('default_temas_id')

    name = fields.Char(string='Clase', tracking=True, required=True,
                       index=True)
    active = fields.Boolean(default=True)
    user_id = fields.Many2one('res.users', string='Profesor',
                              default=lambda self: self.env.uid, index=True,
                              tracking=True)
    description = fields.Html(string='Descripción')
    description_corta = fields.Text(string='Breve descripción')
    priority = fields.Selection(Prioridades_Activas, string='Prioridad',
                                index=True, tracking=True,
                                default=Prioridades_Activas[0][0])
    etiquetas = fields.Many2many('sicpro.app.salon.clases.etiquetas',
                                 'sicpro_app_salon_clases_etiquetas_rel',
                                 string='Etiqueta')
    company_id = fields.Many2one('res.company', string='Proceso',
                                 required=True,
                                 default=lambda self: self.env.company)
    fecha_agregado = fields.Date("Fecha de agregado", index=True,
                                 default=fields.Date.context_today)
    contacto_telefono_fijo = fields.Char(string="Teléfono", )
    contacto_telefono_movil = fields.Char(string="Móvil", )
    contacto_correo = fields.Char(string="Correo electrónico",
                                  related='user_id.email')
    documentacion = fields.Many2many('sicpro.app.salon.clases.adjuntos',
                                     string="Documentación")
    temas_id = fields.Many2one(comodel_name='sicpro.app.salon.clases.temas',
                               string='Temas', required=True)
    displayed_image_id = fields.Many2one(
        'ir.attachment', string='Imagen de portada',
        domain="[('res_model', '=', 'sicpro.app.salon.clases'), "
               "('res_id', '=', id), ('mimetype', 'ilike', 'image')]",)

