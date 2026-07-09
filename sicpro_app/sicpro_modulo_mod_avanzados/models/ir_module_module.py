# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo import api, fields, models, modules, tools
from odoo.addons.base.models.ir_module import assert_log_admin_access
from odoo.addons.sicpro_app_administracion.models.constants import MSG_SOPORTE_SICPRO
import operator


class IrModuleModule(models.Model):
    _inherit = 'ir.module.module'

    local_updatable = fields.Boolean(string='Local updatable', compute=False, default=False, store=True)
    addons_path_id = fields.Many2one('ir.module.addons.path', string='Addons Path ID', readonly=True)
    addons_path = fields.Char(string='Addons Path', related='addons_path_id.path', readonly=True)
    license = fields.Char(readonly=True)
    module_type = fields.Selection(selection_add=[('Daniel Barrero Reyes', 'SICPRO ERP')], default='official')

    def module_multi_uninstall(self):
        modules = self.browse(self.env.context.get('active_ids'))
        [module.button_immediate_uninstall() for module in modules if module not in ['base', 'web']]

    def module_multi_refresh_po(self):
        lang = self.env.user.lang
        modules = self.filtered(lambda r: r.state == 'installed')
        modules._update_translations(filter_lang=lang, overwrite=True)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'target': 'new',
            'params': {
                'message': ("Los idiomas que has seleccionado han sido "
                             "Actualizado con éxito. Aún necesitas actualizar las aplicaciones para que funcione.\n\n" + MSG_SOPORTE_SICPRO),
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    @assert_log_admin_access
    def button_immediate_upgrade(self):
        res = self.module_multi_refresh_po()
        return super(IrModuleModule, self).button_immediate_upgrade()

    def button_get_po(self):
        self.ensure_one()
        action = self.env.ref('sicpro_modulo_mod_avanzados.action_server_module_multi_get_po').sudo().read()[0]
        action['context'].update({
                'default_lang': self.env.user.lang,
            })
        return action

    def update_list(self):
        res = super(IrModuleModule, self).update_list()
        default_version = modules.adapt_version('1.0')
        known_mods = self.with_context(lang=None).search([])
        known_mods_names = {mod.name: mod for mod in known_mods}

        for mod_name in modules.get_modules():
            mod = known_mods_names.get(mod_name)
            if mod:
                installed_version = self.get_module_info(mod.name).get('version', default_version)
                if installed_version and mod.latest_version and operator.gt(installed_version, mod.latest_version):
                    local_updatable = True
                else:
                    local_updatable = False
                if mod.local_updatable != local_updatable:
                    mod.write({'local_updatable': local_updatable})
        return res

    def _update_from_terp(self, terp):
        res = super()._update_from_terp(terp)
        author = terp.get('author')
        if author:
            author = author.lower()
        if author and author in ['odooai.cn', 'Daniel Barrero Reyes']:
            self.module_type = 'Daniel Barrero Reyes'
        return res

    def web_read(self, specification):
        module_type = self.env.context.get('module_type', 'official')
        if module_type == 'Daniel Barrero Reyes':
            self = self.with_context(module_type='official')
        return super(IrModuleModule, self).web_read(specification)
