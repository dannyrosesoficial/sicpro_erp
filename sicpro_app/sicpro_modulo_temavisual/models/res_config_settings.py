from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    background_image = fields.Binary(string="Image de Fondo", attachment=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    theme_background = fields.Binary(string="Imagen de Fondo", related='company_id.background_image', readonly=False)

    def config_color_settings(self):
        colors = {}
        colors['full_bg_img'] = self.env.user.company_id.background_image
        return colors
