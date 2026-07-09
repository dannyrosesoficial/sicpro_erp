# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################
from odoo import http
from odoo.http import request

class WebsiteView(http.Controller):
    """Herencia de http.Controller para añadir rutas personalizadas de encuestas."""

    @http.route('/public/survey', type='http', auth="public", website=True, sitemap=True)
    def public_user_access(self, **kwargs):
        """
        Controlador para listar encuestas públicas en el sitio web.
        Optimizado para Odoo 19 mediante el uso de search_read.
        """
        # Buscamos encuestas que tengan el modo de acceso 'website' y visibilidad habilitada
        # Se añaden campos específicos para evitar cargar todo el objeto en memoria
        surveys = request.env['survey.survey'].sudo().search_read(
            [('access_mode', '=', 'website'), ('visibility', '=', True)],
            ['title', 'attempts_limit', 'create_date', 'access_token']
        )

        # Formateamos los valores para la vista QWeb
        values = {
            'survey_list': [{
                'title': rec['title'],
                'attempts': rec['attempts_limit'],
                'date': rec['create_date'].strftime('%d/%m/%Y') if rec['create_date'] else '',
                'access_token': rec['access_token']
            } for rec in surveys],
        }

        return request.render("enhanced_survey_management.survey_visibility", values)