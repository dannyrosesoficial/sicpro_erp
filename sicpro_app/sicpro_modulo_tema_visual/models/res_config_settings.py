# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @property
    def THEME_COLOR_FIELDS(self):
        return [
            'color_appsmenu_text',
            'color_appbar_text',
            'color_appbar_active',
            'color_appbar_background',
        ]

    @property
    def COLOR_ASSET_THEME_URL(self):
        return '/sicpro_modulo_tema_visual/static/src/scss/colors.scss'
        
    @property
    def COLOR_BUNDLE_THEME_NAME(self):
        return 'web._assets_primary_variables'

    theme_favicon = fields.Binary(related='company_id.favicon',readonly=False)
    # 1. Campo para la interfaz (Sin config_parameter para evitar el error)
    theme_background_image = fields.Binary(string="Fondo de Pantalla Global", )
    # 2. Campo técnico oculto para persistencia (Tipo Char para que Odoo lo acepte)
    theme_background_image_cache = fields.Char(
        config_parameter='sicpro.theme_background_image')

    theme_color_appsmenu_text = fields.Char(
        string='Color del texto del menú de aplicaciones')
    theme_color_appbar_text = fields.Char(
        string='Color del texto de la barra de aplicaciones')
    theme_color_appbar_active = fields.Char(
        string='Color activo de la barra de aplicaciones')
    theme_color_appbar_background = fields.Char(
        string='Color de fondo de la barra de aplicaciones')
    
    def _get_theme_color_values(self):
        return self.env[
            'sicpro_modulo_tema_colores.color_assets_editor'].get_color_variables_values(
            self.COLOR_ASSET_THEME_URL, 
            self.COLOR_BUNDLE_THEME_NAME,
            self.THEME_COLOR_FIELDS
        )
        
    def _set_theme_color_values(self, values):
        colors = self._get_theme_color_values()
        for var, value in colors.items():
            values[f'theme_{var}'] = value
        return values

    def _detect_theme_color_change(self):
        colors = self._get_theme_color_values()
        return any(
            self[f'theme_{var}'] != val
            for var, val in colors.items()
        )

    def _replace_theme_color_values(self):
        variables = [
            {
                'name': field, 
                'value': self[f'theme_{field}']
            }
            for field in self.THEME_COLOR_FIELDS
        ]
        return self.env['sicpro_modulo_tema_colores.color_assets_editor'].replace_color_variables_values(
            self.COLOR_ASSET_THEME_URL, 
            self.COLOR_BUNDLE_THEME_NAME,
            variables
        )

    def _reset_theme_color_assets(self):
        self.env['sicpro_modulo_tema_colores.color_assets_editor'].reset_color_asset(
            self.COLOR_ASSET_THEME_URL, 
            self.COLOR_BUNDLE_THEME_NAME,
        )

    def action_reset_theme_color_assets(self):
        self._reset_light_color_assets()
        self._reset_dark_color_assets()
        self._reset_theme_color_assets()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def get_values(self):
        res = super().get_values()

        # 1. Integración de colores
        res = self._set_theme_color_values(res)

        # 2. Integración de imagen de fondo
        bg_param = self.env['ir.config_parameter'].sudo().get_param(
            'sicpro.theme_background_image')
        res.update(theme_background_image=bg_param, )
        return res

    def set_values(self):
        # Primero ejecutamos el super para guardar parámetros estándar
        super().set_values()

        # 1. Integración de colores
        if self._detect_theme_color_change():
            self._replace_theme_color_values()

        # 2. Integración de imagen de fondo
        # Convertimos el binario a string para guardarlo en ir.config_parameter
        value = self.theme_background_image or False
        if value and isinstance(value, bytes):
            value = value.decode('ascii')

        self.env['ir.config_parameter'].sudo().set_param(
            'sicpro.theme_background_image', value)