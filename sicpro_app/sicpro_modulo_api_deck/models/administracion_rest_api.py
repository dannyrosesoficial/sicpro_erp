# -*- coding: utf-8 -*-


from datetime import datetime

import requests
import base64
from werkzeug.utils import html
from odoo.addons.link_tracker.models.link_tracker import URL_MAX_SIZE
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.http import request
from odoo import models, fields, api, http, _


class AdministracionRestApi(models.Model):
    _inherit = 'sicpro.app.administracion.rest.api'

    name = fields.Selection(
        selection_add=[('sicpro.modulo.deck.sync', 'MÓDULO SYNC DECK API')],
        ondelete={'sicpro.modulo.deck.sync': 'cascade'})

    # IMPORTANTE: El nombre de la acción debe ser 'api_test_' + el nombre
    # del valor del campo name
    def api_test_sicpro_modulo_sync_api_deck(self):
        data = self.env['sicpro.app.administracion.rest.api'].sudo().search(
            [('name', '=', 'sicpro.modulo.deck.sync')])
        url_data = data.url_data
        response = requests.get(url_data, verify=False)

        if response.status_code == 200:
            raise ValidationError(_('Conexión establecida con éxito.'))
        else:
            raise ValidationError(_('Conexión reusada en el url Data. Verifíquelo'))

    # IMPORTANTE: El nombre de la acción debe ser 'api_cron_' + el nombre
    # del valor del campo name
    def api_cron_sicpro_modulo_sync_api_deck(self):
        raise UserError(_('Esta aplicación no posee un cron de ejecución.'))
        # data = self.env['sicpro.app.administracion.rest.api'].sudo().search(
        #     [('name', '=', 'sicpro.modulo.calendario.sync')])
        # url_data = data.url_data
        # app_externa = data.app_externa
        # registros_creados = 0
        # registros_actualizados = 0
        # fecha_inicio = datetime.today()
        #
        # global data_equipos
        #
        # # compruebo la validez de la url
        # response = requests.head(url_data, timeout=5, verify=False)
        # if response.status_code == 200:
        #
        #     registros_actualizados += 1
        #
        #     # actualizo el historial de conexiones
        #     self.env[
        #         'sicpro.app.administracion.rest.api.historial'].sudo().create(
        #         {'name': 'APLICACIÓN DE TRABAJADORES',
        #          'app_externa': app_externa, 'fecha_inicio': fecha_inicio,
        #          'fecha_fin': datetime.today(),
        #          'registros_creados': registros_creados,
        #          'registros_actualizados': registros_actualizados,
        #          'estado': 'exito', })
        # else:
        #     # actualizo el historial de conexiones
        #     self.env[
        #         'sicpro.app.administracion.rest.api.historial'].sudo().create(
        #         {'name': 'APLICACIÓN DE TRANSPORTE',
        #          'app_externa': app_externa, 'fecha_inicio': datetime.today(),
        #          'fecha_fin': datetime.today(), 'registros_creados': 0,
        #          'registros_actualizados': 0, 'estado': 'fallido', })