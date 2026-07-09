# -*- coding: utf-8 -*-


import json
import requests
from odoo import api, models
from odoo.exceptions import _logger


class SicproDeckApi(models.TransientModel):
    _inherit = 'sicpro.modulo.deck.api'

    # agregar usuario a la tarjeta de la columna del board específico
    def api_deck_tarjeta_usuario_modificar(self, usuario, board_id, columna_id, tarjeta_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards/" + str(
            tarjeta_id) + "/assignUser"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la modificación del USUARIO/TARJETA ha fallado, a continuación se"
                    " muestran los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # eliminar usuario a la tarjeta de la columna del board específico
    def api_deck_tarjeta_usuario_eliminar(self, usuario, board_id, columna_id, tarjeta_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards/" + str(
            tarjeta_id) + "/unassignUser"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la eliminación del USUARIO/TARJETA ha fallado, a continuación sé "
                    "muestran los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)