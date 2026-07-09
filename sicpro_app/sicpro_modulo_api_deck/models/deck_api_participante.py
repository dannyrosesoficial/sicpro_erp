# -*- coding: utf-8 -*-


import json
import requests
from odoo import api, models
from odoo.exceptions import _logger


class SicproDeckApi(models.TransientModel):
    _inherit = 'sicpro.modulo.deck.api'

    # agregar participante a la tarjeta de la columna del board específico
    def api_deck_tarjeta_participate_crear(self, usuario, board_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/acl/"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la creación del PARTICIPANTE ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # modificar participante a la tarjeta de la columna del board específico
    def api_deck_tarjeta_participate_modificar(self, usuario, board_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/acl/"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la modificación del PARTICIPANTE ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # eliminar participante a la tarjeta de la columna del board específico
    def api_deck_tarjeta_participate_eliminar(self, usuario, board_id, participante_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/acl/" + str(participante_id)
        payload = ''
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("DELETE", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la eliminación del PARTICIPANTE ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)