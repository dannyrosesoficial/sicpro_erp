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
    def COLOR_FIELDS(self):
        return [
            'color_brand',
            'color_primary',
            'color_success',
            'color_info',
            'color_warning',
            'color_danger',
        ]
        
    @property
    def COLOR_ASSET_LIGHT_URL(self):
        return '/sicpro_modulo_tema_colores/static/src/scss/colors_light.scss'
        
    @property
    def COLOR_BUNDLE_LIGHT_NAME(self):
        return 'web._assets_primary_variables'
        
    @property
    def COLOR_ASSET_DARK_URL(self):
        return '/sicpro_modulo_tema_colores/static/src/scss/colors_dark.scss'
        
    @property
    def COLOR_BUNDLE_DARK_NAME(self):
        return 'web.assets_web_dark'

    # Campos Modo claro
    color_brand_light = fields.Char(string='Color claro de la marca')
    color_primary_light = fields.Char(string='Color claro primario')
    color_success_light = fields.Char(string='Color claro de éxito')
    color_info_light = fields.Char(string='Color claro de Información')
    color_warning_light = fields.Char(string='Color claro de advertencia')
    color_danger_light = fields.Char(string='Color claro de peligro')

    # Campos Modo oscuro
    color_brand_dark = fields.Char(string='Color oscuro de la marca')
    color_primary_dark = fields.Char(string='Color oscuro primario')
    color_success_dark = fields.Char(string='Color oscuro de éxito')
    color_info_dark = fields.Char(string='Color oscuro de Información')
    color_warning_dark = fields.Char(string='Color oscuro de advertencia')
    color_danger_dark = fields.Char(string='Color oscuro de peligro')

    # Ayudante
    def _get_light_color_values(self):
        return self.env['sicpro_modulo_tema_colores.color_assets_editor'].get_color_variables_values(
            self.COLOR_ASSET_LIGHT_URL, 
            self.COLOR_BUNDLE_LIGHT_NAME,
            self.COLOR_FIELDS
        )
        
    def _get_dark_color_values(self):
        return self.env['sicpro_modulo_tema_colores.color_assets_editor'].get_color_variables_values(
            self.COLOR_ASSET_DARK_URL, 
            self.COLOR_BUNDLE_DARK_NAME,
            self.COLOR_FIELDS
        )
        
    def _set_light_color_values(self, values):
        colors = self._get_light_color_values()
        for var, value in colors.items():
            values[f'{var}_light'] = value
        return values
        
    def _set_dark_color_values(self, values):
        colors = self._get_dark_color_values()
        for var, value in colors.items():
            values[f'{var}_dark'] = value
        return values
    
    def _detect_light_color_change(self):
        colors = self._get_light_color_values()
        return any(
            self[f'{var}_light'] != val
            for var, val in colors.items()
        )
        
    def _detect_dark_color_change(self):
        colors = self._get_dark_color_values()
        return any(
            self[f'{var}_dark'] != val
            for var, val in colors.items()
        )
        
    def _replace_light_color_values(self):
        variables = [
            {
                'name': field, 
                'value': self[f'{field}_light']
            }
            for field in self.COLOR_FIELDS
        ]
        return self.env['sicpro_modulo_tema_colores.color_assets_editor'].replace_color_variables_values(
            self.COLOR_ASSET_LIGHT_URL, 
            self.COLOR_BUNDLE_LIGHT_NAME,
            variables
        )
        
    def _replace_dark_color_values(self):
        variables = [
            {
                'name': field, 
                'value': self[f'{field}_dark']
            }
            for field in self.COLOR_FIELDS
        ]
        return self.env['sicpro_modulo_tema_colores.color_assets_editor'].replace_color_variables_values(
            self.COLOR_ASSET_DARK_URL, 
            self.COLOR_BUNDLE_DARK_NAME,
            variables
        )
    
    def _reset_light_color_assets(self):
        self.env['sicpro_modulo_tema_colores.color_assets_editor'].reset_color_asset(
            self.COLOR_ASSET_LIGHT_URL, 
            self.COLOR_BUNDLE_LIGHT_NAME,
        )
        
    def _reset_dark_color_assets(self):
        self.env['sicpro_modulo_tema_colores.color_assets_editor'].reset_color_asset(
            self.COLOR_ASSET_DARK_URL, 
            self.COLOR_BUNDLE_DARK_NAME,
        )

    # Acción
    def action_reset_light_color_assets(self):
        self._reset_light_color_assets()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    
    def action_reset_dark_color_assets(self):
        self._reset_dark_color_assets()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    # Funciones
    def get_values(self):
        res = super().get_values()
        res = self._set_light_color_values(res)
        res = self._set_dark_color_values(res)
        return res

    def set_values(self):
        res = super().set_values()
        if self._detect_light_color_change():
            self._replace_light_color_values()
        if self._detect_dark_color_change():
            self._replace_dark_color_values()
        return res
