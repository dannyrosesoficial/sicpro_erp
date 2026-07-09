# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    app_system_name = fields.Char(
        'Nombre del sistema', help="Configurar el nombre del sistema, que "
                                   "reemplaza a Odoo")
    app_show_lang = fields.Boolean('Mostrar Selector de Lenguajes',
                                   help="Cuando se habilita, el usuario "
                                        "puede cambiar rápidamente el idioma "
                                        "en el menú "
                                        "del usuario")
    app_show_debug = fields.Boolean('Mostrar depuración rápida',
                                    help="Cuando se habilita, todos los "
                                         "usuarios pueden ver el menú de "
                                         "depuración")
    app_show_documentation = fields.Boolean('Mostrar documentación',
                                            help="Cuando se habilita, el "
                                                 "usuario puede visitar el "
                                                 "manual del usuario")
    app_show_documentation_dev = fields.Boolean(
        'Mostrar planillas de accesos',
        help="Cuando se habilita, "
             "el usuario puede "
             "visitar la "
             "planilla de "
             " accesos")
    app_show_support = fields.Boolean('Mostrar soporte',
                                      help="Cuando se habilita, el usuario "
                                           "puede visitar su sitio de "
                                           "soporte")
    app_show_account = fields.Boolean('Mostrar Plataforma de VideoConferencias',
                                      help="Cuando se habilita, el usuario "
                                           "puede iniciar sesión en su sitio"
                                           " web")
    app_show_enterprise = fields.Boolean('Mostrar etiqueta de empresa',
                                         help="Desmarque para ocultar la "
                                              "etiqueta Enterprise")
    app_show_share = fields.Boolean('Mostrar panel de control compartido',
                                    help="Desmarque para ocultar el Panel de "
                                         "control de Odoo Share")
    app_show_poweredby = fields.Boolean('Mostrar Desarrollado por Odoo',
                                        help="Desmarque para ocultar el "
                                             "texto Desarrollado por")
    group_show_author_in_apps = fields.Boolean(
        string="Mostrar autor en el Panel de aplicaciones",
        implied_group='sicpro_modulo_avanzado.group_show_author_in_apps',
        help="Desmarque para ocultar el autor y el sitio web en el panel de"
             " aplicaciones")

    app_documentation_url = fields.Char('URL de documentación')
    app_documentation_dev_url = fields.Char('URL de planilla de accesos')
    app_support_url = fields.Char('Url de soporte')
    app_account_title = fields.Char('Plataforma de VideoConferencias')
    app_account_url = fields.Char('Mi URL de mi cuenta')
    app_enterprise_url = fields.Char('Personalizar URL del módulo (por '
                                     'ejemplo, Enterprise)')


    module_odoo_referral = fields.Boolean('Show Odoo Referral',
                                          help="Uncheck to remove the Odoo Referral")

    app_ribbon_name = fields.Char('Ver Ribbon Prueba')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        app_system_name = ir_config.get_param('app_system_name', default='SICPRO ERP')

        app_show_lang = True if ir_config.get_param('app_show_lang') == "True" else False
        app_show_debug = True if ir_config.get_param('app_show_debug') == "True" else False
        app_show_documentation = True if ir_config.get_param('app_show_documentation') == "True" else False
        app_show_documentation_dev = True if ir_config.get_param('app_show_documentation_dev') == "True" else False
        app_show_support = True if ir_config.get_param('app_show_support') == "True" else False
        app_show_account = True if ir_config.get_param('app_show_account') == "True" else False
        app_show_enterprise = True if ir_config.get_param('app_show_enterprise') == "True" else False
        app_show_share = True if ir_config.get_param('app_show_share') == "True" else False
        app_show_poweredby = True if ir_config.get_param('app_show_poweredby') == "True" else False

        app_documentation_url = ir_config.get_param('app_documentation_url',
                                                    default='#')
        app_documentation_dev_url = ir_config.get_param('app_documentation_dev_url',
                                                        default='#')
        app_support_url = ir_config.get_param('app_support_url', default='#')
        app_account_title = ir_config.get_param('app_account_title', default='Mi cuenta SICPRO')
        app_account_url = ir_config.get_param('app_account_url', default='#')
        app_enterprise_url = ir_config.get_param('app_enterprise_url', default='#')
        app_ribbon_name = ir_config.get_param('app_ribbon_name', default='*Sunpop.cn')
        res.update(
            app_system_name=app_system_name,
            app_show_lang=app_show_lang,
            app_show_debug=app_show_debug,
            app_show_documentation=app_show_documentation,
            app_show_documentation_dev=app_show_documentation_dev,
            app_show_support=app_show_support,
            app_show_account=app_show_account,
            app_show_enterprise=app_show_enterprise,
            app_show_share=app_show_share,
            app_show_poweredby=app_show_poweredby,

            app_documentation_url=app_documentation_url,
            app_documentation_dev_url=app_documentation_dev_url,
            app_support_url=app_support_url,
            app_account_title=app_account_title,
            app_account_url=app_account_url,
            app_enterprise_url=app_enterprise_url,
            app_ribbon_name=app_ribbon_name
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param("app_system_name", self.app_system_name or "")
        ir_config.set_param("app_show_lang", self.app_show_lang or "False")
        ir_config.set_param("app_show_debug", self.app_show_debug or "False")
        ir_config.set_param("app_show_documentation", self.app_show_documentation or "False")
        ir_config.set_param("app_show_documentation_dev", self.app_show_documentation_dev or "False")
        ir_config.set_param("app_show_support", self.app_show_support or "False")
        ir_config.set_param("app_show_account", self.app_show_account or "False")
        ir_config.set_param("app_show_enterprise", self.app_show_enterprise or "False")
        ir_config.set_param("app_show_share", self.app_show_share or "False")
        ir_config.set_param("app_show_poweredby", self.app_show_poweredby or "False")

        ir_config.set_param("app_documentation_url",
                            self.app_documentation_url or "#")
        ir_config.set_param("app_documentation_dev_url",
                            self.app_documentation_dev_url or "#")
        ir_config.set_param("app_support_url", self.app_support_url or "#")
        ir_config.set_param("app_account_title", self.app_account_title or "Mi cuenta SICPRO")
        ir_config.set_param("app_account_url", self.app_account_url or "#")
        ir_config.set_param("app_enterprise_url", self.app_enterprise_url or "#")
        ir_config.set_param("app_ribbon_name", self.app_ribbon_name or "*Sunpop.cn")

    def set_module_url(self):
        sql = "UPDATE ir_module_module SET website = '%s' WHERE license like '%s' and website <> ''" % (self.app_enterprise_url, 'OEEL%')
        try:
            self._cr.execute(sql)
            self._cr.commit()
        except Exception as e:
            pass
