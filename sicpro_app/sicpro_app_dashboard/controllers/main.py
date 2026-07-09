# -*- coding: utf-8 -*-


from lxml import etree as ElementTree

from odoo.http import Controller, route, request


class DashBoard(Controller):

    @route('/sicpro_app_dashboard/add_to_dashboard', type='json', auth='user')
    def add_to_dashboard(self, action_id, context_to_save, domain, view_mode, name=''):
        action = request.env.ref('sicpro_app_dashboard.mi_dashboards_action').sudo()

        if action and action['res_model'] == 'sicpro.app.dashboard' and action['views'][0][1] == 'form' and action_id:
            view_id = action['views'][0][0]
            board = request.env['sicpro.app.dashboard'].fields_view_get(view_id, 'form')
            if board and 'arch' in board:
                xml = ElementTree.fromstring(board['arch'])
                column = xml.find('./board/column')
                if column is not None:
                    new_action = ElementTree.Element('action', {
                        'name': str(action_id),
                        'string': name,
                        'view_mode': view_mode,
                        'context': str(context_to_save),
                        'domain': str(domain)
                    })
                    column.insert(0, new_action)
                    arch = ElementTree.tostring(xml, encoding='unicode')
                    request.env['ir.ui.view.custom'].create({
                        'user_id': request.session.uid,
                        # filtro de la aplicación actual
                        'aplicacion_filtro': 'sicpro_app_dashboard',
                        'ref_id': view_id,
                        'arch': arch
                    })
                    return True

        return False
