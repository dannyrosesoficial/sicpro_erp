# -*- coding: utf-8 -*-


import json
import requests
from odoo import api, models
from odoo.exceptions import _logger


class SicproDeckApi(models.TransientModel):
    _inherit = 'sicpro.modulo.deck.api'

    # busca todas las columnas del board específico
    def api_deck_estado_buscar_todos(self, usuario, board_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks"
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
            return ("Deck API: La ejecución de la búsqueda de todos los ESTADOS ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # busca una columna del board específico
    def api_deck_estado_buscar_id(self, usuario, board_id, columna_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id)
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
            return ("Deck API: La ejecución de la búsqueda del ESTADO específico ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # crear una columna del board
    def api_deck_estado_crear(self, usuario, board_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))
            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la creación del ESTADO ha fallado, a continuación se muestran los datos:"
                    " %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # actualizar una columna del board
    def api_deck_estado_modificar(self, usuario, board_id, columna_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id)
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))
            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la modificación del ESTADO ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # elimina una columna del board
    def api_deck_estado_eliminar(self, usuario, board_id, columna_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/stacks/" + str(columna_id)
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
            return ("Deck API: La ejecución de la eliminación del ESTADO ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)
