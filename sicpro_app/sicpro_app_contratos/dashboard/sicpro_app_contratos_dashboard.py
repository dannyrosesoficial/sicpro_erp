# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.http import request


class VistaCustom(models.Model):
    _inherit = 'ir.ui.view.custom'

    aplicacion_filtro = fields.Char(string='aplicación')


class ContratosDashboard(models.AbstractModel):
    _name = 'sicpro.app.contratos.dashboard'
    _description = "Dashboard de Contratos"
    _auto = False

    @api.model
    def create(self, vals):
        return self

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):

        res = super(ContratosDashboard, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        custom_view = self.env['ir.ui.view.custom'].search(
            [('aplicacion_filtro', '=', 'sicpro_app_contratos'),
                ('ref_id', '=', view_id)], limit=1)
        if custom_view:
            res.update(
                {'custom_view_id': custom_view.id, 'arch': custom_view.arch})
        res.update({'arch': self._arch_preprocessing(res['arch']),
                    'toolbar': {'print': [], 'action': [], 'relate': []}})
        return res

    @api.model
    def _arch_preprocessing(self, arch):
        from lxml import etree

        def remove_unauthorized_children(node):
            for child in node.iterchildren():
                if child.tag == 'action' and child.get('invisible'):
                    node.remove(child)
                else:
                    remove_unauthorized_children(child)
            return node

        archnode = etree.fromstring(arch)
        archnode.set('js_class', 'board')
        return etree.tostring(remove_unauthorized_children(archnode),
                              pretty_print=True, encoding='unicode')

    @api.model
    def check_user_group(self):
        uid = request.session.uid
        user = self.env['res.users'].sudo().search([('id', '=', uid)], limit=1)
        if user.has_group(
                'sicpro_app_contratos.grupo_app_contratos_dashboard_admin'):
            return {'groups': True}
        else:
            return {'groups': False}
