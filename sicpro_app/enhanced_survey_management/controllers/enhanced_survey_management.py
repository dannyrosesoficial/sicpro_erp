# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import request


class SurveyLoadContent(http.Controller):
    """Controller to load country and state to the survey"""

    @http.route('/survey/load_country', type="json", auth="public", website=True, csrf=False)
    def load_country(self):
        """
        Retorna nombres e IDs de países.
        Optimizado para usar search_read y mejorar el rendimiento en Odoo 19.
        """
        countries = request.env['res.country'].sudo().search_read([], ['id', 'name'])
        return {'id': [c['id'] for c in countries], 'name': [c['name'] for c in countries], }

    @http.route('/survey/load_states', type="json", auth="public", website=True, csrf=False)
    def load_states(self, country_id=None, **kwargs):
        """
        Retorna estados basados en el país.
        Se ajusta para recibir 'country_id' directamente desde el JSON RPC.
        """
        # En Odoo 19, si el JS envía {country_id: 'valor'}, llega como argumento.
        # Si llega dentro de params (legacy), lo extraemos.
        c_name = country_id or kwargs.get('params', {}).get('country_id')

        if not c_name:
            return {'id': [], 'name': []}

        country = request.env['res.country'].sudo().search([('name', '=', c_name)], limit=1)

        if not country:
            return {'id': [], 'name': []}

        states = request.env['res.country.state'].sudo().search_read([('country_id', '=', country.id)], ['id', 'name'])

        return {'id': [s['id'] for s in states], 'name': [s['name'] for s in states], }
