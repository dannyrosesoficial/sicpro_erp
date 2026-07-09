# -*- coding: utf-8 -*-


import json
import requests
from odoo import api, models
from odoo.exceptions import _logger


class SicproDeckApi(models.TransientModel):
    _inherit = 'sicpro.modulo.deck.api'

    # busca la tarjeta de la columna del board específico
    def api_deck_tarjeta_buscar_id(self, usuario, board_id, columna_id, tarjeta_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards/" + str(tarjeta_id)
        payload = {}
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("GET", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la búsqueda de la TARJETA especifica ha fallado, a continuación se"
                    " muestran los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # crear la tarjeta de la columna del board específico
    def api_deck_tarjeta_crear(self, usuario, board_id, columna_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la creación de la TARJETA ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # actualizar la tarjeta de la columna del board específico (NO A FUNCIONADO REVISAR)
    def api_deck_tarjeta_modificar(self, usuario, board_id, columna_id, tarjeta_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards/" + str(tarjeta_id)
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la modificción de la TARJETA ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # eliminar la tarjeta de la columna del board específico
    def api_deck_tarjeta_eliminar(self, usuario, board_id, columna_id, tarjeta_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "https://nube.etecsa.cu/index.php/apps/deck/api/v1.0/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards/" + str(tarjeta_id)
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
            return ("Deck API: La ejecución de la eliminación de la TARJETA ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)