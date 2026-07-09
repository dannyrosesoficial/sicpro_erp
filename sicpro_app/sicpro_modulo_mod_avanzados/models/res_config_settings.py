# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    app_system_name = fields.Char(string='Nombre del sistema',
                                  help="Nombre del sistema de configuración.",
                                  default='SICPRO ERP',
                                  config_parameter='app_system_name')
    app_show_lang = fields.Boolean(string='Cambiar rápido de idioma',
                                   help="Cuando está habilitado, el usuario puede cambiar rápidamente de idioma en el menú de usuario",
                                   config_parameter='app_show_lang')
    app_show_debug = fields.Boolean(string='Depuración rápida de mostrar',
                                    help="Cuando se habilita, todos los inicios de sesión pueden ver el menú de depuración",
                                    config_parameter='app_show_debug')
    app_show_documentation = fields.Boolean(string='Mostrar Documentación',
                                            help="Cuando esté habilitado, el usuario puede visitar el manual de usuario",
                                            config_parameter='app_show_documentation')

    app_show_documentation_dev = fields.Boolean(string='Mostrar documentación del desarrollador',
        help="Cuando esté habilitado, el usuario puede consultar la documentación de desarrollo")
    app_show_support = fields.Boolean(string='Soporte del programa',
                                      help="Cuando se habilita, el usuario puede visitar tu sitio de soporte",
                                      config_parameter='app_show_support')
    app_show_account = fields.Boolean(string='Mostrar mi cuenta',
                                      help="Cuando está habilitado, el usuario puede iniciar sesión en tu sitio web",
                                      config_parameter='app_show_account')
    app_show_enterprise = fields.Boolean(string='Etiqueta de Mostrar Empresa',
                                         help="Desmarca para ocultar la etiqueta Enterprise",
                                         config_parameter='app_show_enterprise')
    app_show_share = fields.Boolean(string='Mostrar panel de compartición',
                                    help="Desmarca para ocultar el Panel de Odoo Share",
                                    config_parameter='app_show_share')
    app_show_poweredby = fields.Boolean(string='Programa impulsado por Odoo',
                                        help="Desmarca para ocultar el texto Powered by",
                                        config_parameter='app_show_poweredby')
    group_show_author_in_apps = fields.Boolean(
        string="Mostrar autor en el panel de Apps",
        implied_group='base.group_system',
        help="Desmarcar para ocultar autor y sitio web en el panel de aplicaciones")
    app_show_odoo_referral = fields.Boolean(string='Mostrar referencia de Odoo',
                                            help="Desmarque para eliminar la referencia de Odoo")

    app_documentation_url = fields.Char(string='URL de documentación',
                                        config_parameter='app_documentation_url')
    app_documentation_dev_url = fields.Char(string='URL de documentación del desarrollador',
        config_parameter='app_documentation_dev_url')
    app_support_url = fields.Char(string='URL de soporte',
                                  config_parameter='app_support_url')
    app_account_title = fields.Char(string='Título de la cuenta',
                                    config_parameter='app_account_title')
    app_account_url = fields.Char(string='URL de la cuenta',
                                  config_parameter='app_account_url')
    app_ribbon_name = fields.Char(string='Mostrar cinta',
                                  config_parameter='app_ribbon_name')
    app_navbar_pos_pc = fields.Selection(string="Barra de navegación PC",
                                         selection=[('top', 'Top(Default)'),
                                             ('bottom', 'Bottom'),
                                             # ('left', 'Left'),
                                         ],
                                         config_parameter='app_navbar_pos_pc')
    app_navbar_pos_mobile = fields.Selection(
        string="Barra de navegación móvil",
        selection=[('top', 'Top(Default)'), ('bottom', 'Bottom'),
                   # ('left', 'Left'),
                   ], config_parameter='app_navbar_pos_mobile')
    app_doc_root_url = fields.Char(string='Ayuda del dominio del tema',
                                   config_parameter='app_doc_root_url',
                                   default='https://sicproerp.dvpe.etecsa.cu')

    def action_set_app_doc_root_to_my(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        self.app_doc_root_url = base_url
