# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    app_system_name = fields.Char('Nombre del sistema', help="Configurar el nombre del sistema")
    app_ribbon_name = fields.Char('Ver Ribbon Prueba')

    app_menu_perfil_1 = fields.Boolean('Activar Menu Perfil 1')
    app_menu_perfil_1_titulo = fields.Char('Titulo Menu Perfil 1')
    app_menu_perfil_1_url = fields.Char('Url Menu Perfil 1')
    app_menu_perfil_1_sequence = fields.Integer('Secuencia Menu Perfil 1')
    app_menu_perfil_2 = fields.Boolean('Activar Menu Perfil 2')
    app_menu_perfil_2_titulo = fields.Char('Titulo Menu Perfil 2')
    app_menu_perfil_2_url = fields.Char('Url Menu Perfil 2')
    app_menu_perfil_2_sequence = fields.Integer('Secuencia Menu Perfil 2')
    app_menu_perfil_3 = fields.Boolean('Activar Menu Perfil 3')
    app_menu_perfil_3_titulo = fields.Char('Titulo Menu Perfil 3')
    app_menu_perfil_3_url = fields.Char('Url Menu Perfil 3')
    app_menu_perfil_3_sequence = fields.Integer('Secuencia Menu Perfil 3')
    app_menu_perfil_4 = fields.Boolean('Activar Menu Perfil 4')
    app_menu_perfil_4_titulo = fields.Char('Titulo Menu Perfil 4')
    app_menu_perfil_4_url = fields.Char('Url Menu Perfil 4')
    app_menu_perfil_4_sequence = fields.Integer('Secuencia Menu Perfil 4')
    app_menu_perfil_5 = fields.Boolean('Activar Menu Perfil 5')
    app_menu_perfil_5_titulo = fields.Char('Titulo Menu Perfil 5')
    app_menu_perfil_5_url = fields.Char('Url Menu Perfil 5')
    app_menu_perfil_5_sequence = fields.Integer('Secuencia Menu Perfil 5')
    app_menu_perfil_6 = fields.Boolean('Activar Menu Perfil 6')
    app_menu_perfil_6_titulo = fields.Char('Titulo Menu Perfil 6')
    app_menu_perfil_6_url = fields.Char('Url Menu Perfil 6')
    app_menu_perfil_6_sequence = fields.Integer('Secuencia Menu Perfil 6')
    app_menu_separador_1 = fields.Boolean('Activar Menu Separador 1')
    app_menu_separador_1_sequence = fields.Integer('Secuencia Menu Separador 1')
    app_menu_separador_2 = fields.Boolean('Activar Menu Separador 2')
    app_menu_separador_2_sequence = fields.Integer('Secuencia Menu Separador 2')
    app_menu_separador_3 = fields.Boolean('Activar Menu Separador 3')
    app_menu_separador_3_sequence = fields.Integer('Secuencia Menu Separador 3')
    app_menu_separador_4 = fields.Boolean('Activar Menu Separador 4')
    app_menu_separador_4_sequence = fields.Integer('Secuencia Menu Separador 4')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        app_system_name = ir_config.get_param('app_system_name', default='SICPRO ERP')
        app_ribbon_name = ir_config.get_param('app_ribbon_name', default='False')
        app_menu_perfil_1 = True if ir_config.get_param('app_menu_perfil_1') == "True" else False
        app_menu_perfil_1_titulo = ir_config.get_param('app_menu_perfil_1_titulo')
        app_menu_perfil_1_url = ir_config.get_param('app_menu_perfil_1_url')
        app_menu_perfil_1_sequence = ir_config.get_param('app_menu_perfil_1_sequence')
        app_menu_perfil_2 = True if ir_config.get_param('app_menu_perfil_2') == "True" else False
        app_menu_perfil_2_titulo = ir_config.get_param('app_menu_perfil_2_titulo')
        app_menu_perfil_2_url = ir_config.get_param('app_menu_perfil_2_url')
        app_menu_perfil_2_sequence = ir_config.get_param('app_menu_perfil_2_sequence')
        app_menu_perfil_3 = True if ir_config.get_param('app_menu_perfil_3') == "True" else False
        app_menu_perfil_3_titulo = ir_config.get_param('app_menu_perfil_3_titulo')
        app_menu_perfil_3_url = ir_config.get_param('app_menu_perfil_3_url')
        app_menu_perfil_3_sequence = ir_config.get_param('app_menu_perfil_3_sequence')
        app_menu_perfil_4 = True if ir_config.get_param('app_menu_perfil_4') == "True" else False
        app_menu_perfil_4_titulo = ir_config.get_param('app_menu_perfil_4_titulo')
        app_menu_perfil_4_url = ir_config.get_param('app_menu_perfil_4_url')
        app_menu_perfil_4_sequence = ir_config.get_param('app_menu_perfil_4_sequence')
        app_menu_perfil_5 = True if ir_config.get_param('app_menu_perfil_5') == "True" else False
        app_menu_perfil_5_titulo = ir_config.get_param('app_menu_perfil_5_titulo')
        app_menu_perfil_5_url = ir_config.get_param('app_menu_perfil_5_url')
        app_menu_perfil_5_sequence = ir_config.get_param('app_menu_perfil_5_sequence')
        app_menu_perfil_6 = True if ir_config.get_param('app_menu_perfil_6') == "True" else False
        app_menu_perfil_6_titulo = ir_config.get_param('app_menu_perfil_6_titulo')
        app_menu_perfil_6_url = ir_config.get_param('app_menu_perfil_6_url')
        app_menu_perfil_6_sequence = ir_config.get_param('app_menu_perfil_6_sequence')
        app_menu_separador_1 = True if ir_config.get_param('app_menu_separador_1') == "True" else False
        app_menu_separador_1_sequence = ir_config.get_param('app_menu_separador_1_sequence')
        app_menu_separador_2 = True if ir_config.get_param('app_menu_separador_2') == "True" else False
        app_menu_separador_2_sequence = ir_config.get_param('app_menu_separador_2_sequence')
        app_menu_separador_3 = True if ir_config.get_param('app_menu_separador_3') == "True" else False
        app_menu_separador_3_sequence = ir_config.get_param('app_menu_separador_3_sequence')
        app_menu_separador_4 = True if ir_config.get_param('app_menu_separador_4') == "True" else False
        app_menu_separador_4_sequence = ir_config.get_param('app_menu_separador_4_sequence')

        res.update(
            app_system_name=app_system_name,
            app_ribbon_name=app_ribbon_name,
            app_menu_perfil_1=app_menu_perfil_1,
            app_menu_perfil_1_titulo=app_menu_perfil_1_titulo,
            app_menu_perfil_1_url=app_menu_perfil_1_url,
            app_menu_perfil_1_sequence=app_menu_perfil_1_sequence,
            app_menu_perfil_2=app_menu_perfil_2,
            app_menu_perfil_2_titulo=app_menu_perfil_2_titulo,
            app_menu_perfil_2_url=app_menu_perfil_2_url,
            app_menu_perfil_2_sequence=app_menu_perfil_2_sequence,
            app_menu_perfil_3=app_menu_perfil_3,
            app_menu_perfil_3_titulo=app_menu_perfil_3_titulo,
            app_menu_perfil_3_url=app_menu_perfil_3_url,
            app_menu_perfil_3_sequence=app_menu_perfil_3_sequence,
            app_menu_perfil_4=app_menu_perfil_4,
            app_menu_perfil_4_titulo=app_menu_perfil_4_titulo,
            app_menu_perfil_4_url=app_menu_perfil_4_url,
            app_menu_perfil_4_sequence=app_menu_perfil_4_sequence,
            app_menu_perfil_5=app_menu_perfil_5,
            app_menu_perfil_5_titulo=app_menu_perfil_5_titulo,
            app_menu_perfil_5_url=app_menu_perfil_5_url,
            app_menu_perfil_5_sequence=app_menu_perfil_5_sequence,
            app_menu_perfil_6=app_menu_perfil_6,
            app_menu_perfil_6_titulo=app_menu_perfil_6_titulo,
            app_menu_perfil_6_url=app_menu_perfil_6_url,
            app_menu_perfil_6_sequence=app_menu_perfil_6_sequence,
            app_menu_separador_1=app_menu_separador_1,
            app_menu_separador_1_sequence=app_menu_separador_1_sequence,
            app_menu_separador_2=app_menu_separador_2,
            app_menu_separador_2_sequence=app_menu_separador_2_sequence,
            app_menu_separador_3=app_menu_separador_3,
            app_menu_separador_3_sequence=app_menu_separador_3_sequence,
            app_menu_separador_4=app_menu_separador_4,
            app_menu_separador_4_sequence=app_menu_separador_4_sequence,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        ir_config.set_param("app_system_name", self.app_system_name or "")
        ir_config.set_param("app_ribbon_name", self.app_ribbon_name or "False")
        ir_config.set_param("app_menu_perfil_1", self.app_menu_perfil_1 or "False")
        ir_config.set_param("app_menu_perfil_1_titulo", self.app_menu_perfil_1_titulo or "")
        ir_config.set_param("app_menu_perfil_1_url", self.app_menu_perfil_1_url or "")
        ir_config.set_param("app_menu_perfil_1_sequence", self.app_menu_perfil_1_sequence or 0)
        ir_config.set_param("app_menu_perfil_2", self.app_menu_perfil_2 or "False")
        ir_config.set_param("app_menu_perfil_2_titulo", self.app_menu_perfil_2_titulo or "")
        ir_config.set_param("app_menu_perfil_2_url", self.app_menu_perfil_2_url or "")
        ir_config.set_param("app_menu_perfil_2_sequence", self.app_menu_perfil_2_sequence or 0)
        ir_config.set_param("app_menu_perfil_3", self.app_menu_perfil_3 or "False")
        ir_config.set_param("app_menu_perfil_3_titulo", self.app_menu_perfil_3_titulo or "")
        ir_config.set_param("app_menu_perfil_3_url", self.app_menu_perfil_3_url or "")
        ir_config.set_param("app_menu_perfil_3_sequence", self.app_menu_perfil_3_sequence or 0)
        ir_config.set_param("app_menu_perfil_4", self.app_menu_perfil_4 or "False")
        ir_config.set_param("app_menu_perfil_4_titulo", self.app_menu_perfil_4_titulo or "")
        ir_config.set_param("app_menu_perfil_4_url", self.app_menu_perfil_4_url or "")
        ir_config.set_param("app_menu_perfil_4_sequence", self.app_menu_perfil_4_sequence or 0)
        ir_config.set_param("app_menu_perfil_5", self.app_menu_perfil_5 or "False")
        ir_config.set_param("app_menu_perfil_5_titulo", self.app_menu_perfil_5_titulo or "")
        ir_config.set_param("app_menu_perfil_5_url", self.app_menu_perfil_5_url or "")
        ir_config.set_param("app_menu_perfil_5_sequence", self.app_menu_perfil_5_sequence or 0)
        ir_config.set_param("app_menu_perfil_6", self.app_menu_perfil_6 or "False")
        ir_config.set_param("app_menu_perfil_6_titulo", self.app_menu_perfil_6_titulo or "")
        ir_config.set_param("app_menu_perfil_6_url", self.app_menu_perfil_6_url or "")
        ir_config.set_param("app_menu_perfil_6_sequence", self.app_menu_perfil_6_sequence or 0)
        ir_config.set_param("app_menu_separador_1", self.app_menu_separador_1 or "False")
        ir_config.set_param("app_menu_separador_1_sequence", self.app_menu_separador_1_sequence or 0)
        ir_config.set_param("app_menu_separador_2", self.app_menu_separador_2 or "False")
        ir_config.set_param("app_menu_separador_2_sequence", self.app_menu_separador_2_sequence or 0)
        ir_config.set_param("app_menu_separador_3", self.app_menu_separador_3 or "False")
        ir_config.set_param("app_menu_separador_3_sequence", self.app_menu_separador_3_sequence or 0)
        ir_config.set_param("app_menu_separador_4", self.app_menu_separador_4 or "False")
        ir_config.set_param("app_menu_separador_4_sequence", self.app_menu_separador_4_sequence or 0)
