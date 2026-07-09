# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SicproConfigLoginVersion(models.Model):
    _name = 'sicpro.app.login.config.version'
    _description = 'Configuración de la Version de la Aplicación'

    name = fields.Char(string='Versión', required=True)
    config = fields.Char(required=True, default='config_version',
                         readonly=True)

    _sql_constraints = [('name_company_uniq', 'unique(config)',
                         'Ya existe la configuración de Redes Sociales'), ]


class SicproConfigLoginSociales(models.Model):
    _name = 'sicpro.app.login.config.sociales'
    _description = 'Configuración de las Redes Sociales de la Aplicación'

    name = fields.Char(string='config', required=True,
                       default='config_redes_sociales', readonly=True)
    config = fields.Char(required=True, default='config_version',
                         readonly=True)
    facebook = fields.Char(string='Facebook', required=True,
                           default='https://www.facebook.com/etecsa.dvpe/')
    twitter = fields.Char(string='Twitter', required=True,
                          default='https://twitter.com/Etecsa_dvpe/')
    linkedin = fields.Char(string='Linkedin', required=True,
                           default='https://www.linkedin.com/company/etecsa-dvpe/')
    instagram = fields.Char(string='Instagram', required=True,
                            default='https://www.instagram.com/etecsa_dvpe/')
    telegram = fields.Char(string='Telegram', required=True,
                           default='https://t.me/etecsa_dvpe/')
    plantilla_acceso = fields.Char(string='Plantilla Permisos de Acceso',
                                   required=True,
                                   default='https://nube.etecsa.cu/s/CBgjjFrxRgiSgNd')

    _sql_constraints = [('name_company_uniq', 'unique(config)',
                         'Ya existe la configuración de Redes Sociales'), ]
