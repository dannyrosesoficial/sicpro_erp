# -*- coding: utf-8 -*-


import json
import requests
from odoo import api, models
from odoo.exceptions import UserError, ValidationError, _logger


class SicproDeckApi(models.TransientModel):
    _name = 'sicpro.modulo.deck.api'
    _description = 'Modelo de Integración Deck API'

    # buscar el url de la aplicación externa
    def api_deck_url(self):
        url = self.env['sicpro.app.administracion.rest.api'].sudo().search([('name', '=', 'sicpro.modulo.deck.sync')])
        return url

    # modificar configuración del deck para las opciones del calendario
    def api_deck_config(self, usuario):
        url_data = self.api_deck_url().url_data
        url = url_data + "/config/calendar"
        payload = json.dumps({"value": False, })
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))
            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la configuración ha fallado, código: %r, msg: %r, contenido: %r",
                    e.response.status_code, e.response.reason, e.response.content)