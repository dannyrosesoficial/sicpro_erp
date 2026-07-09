# -*- coding: utf-8 -*-


import json
import requests
from odoo import api, models
from odoo.exceptions import _logger


class SicproDeckApi(models.TransientModel):
    _inherit = 'sicpro.modulo.deck.api'

    # buscar etiqueta en el board específico
    def api_deck_board_etiquetas_buscar_id(self, usuario, board_id, etiqueta_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/v1.0/boards/" + str(board_id) + "/labels/" + str(etiqueta_id)
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
            return ("Deck API: La ejecución de la búsqueda de la ETIQUETA específica, ha fallado, a continuación"
                    " se muestran los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # crear etiqueta en el board específico
    def api_deck_board_etiquetas_crear(self, usuario, board_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/labels"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la creación de la ETIQUETA ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # modificar etiqueta en el board específico
    def api_deck_board_etiquetas_modificar(self, usuario, board_id, etiqueta_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/labels/" + str(etiqueta_id)
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la modificación de la ETIQUETA ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # eliminar etiqueta en el board específico
    def api_deck_board_etiquetas_eliminar(self, usuario, board_id, etiqueta_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/labels/" + str(etiqueta_id)
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
            return ("Deck API: La ejecución de la eliminación de la ETIQUETA ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # actualizar etiqueta en la tarjeta de la columna del board específico
    def api_deck_tarjeta_etiquetas_modificar(self, usuario, board_id, columna_id, tarjeta_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards/" + str(tarjeta_id) + "/assignLabel"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))
            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la modificación de la ETIQUETA/TARJETA ha fallado, a continuación se"
                    " muestran los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # eliminar etiqueta en la tarjeta de la columna del board específico
    def api_deck_tarjeta_etiquetas_eliminar(self, usuario, board_id, columna_id, tarjeta_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id) + "/cards/" + str(tarjeta_id) + "/removeLabel"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))
            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la eliminación de la ETIQUETA/TARJETA ha fallado, a continuación se"
                    " muestran los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)