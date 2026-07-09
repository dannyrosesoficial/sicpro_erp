# -*- coding: utf-8 -*-


import json
import requests
from odoo import api, models
from odoo.exceptions import _logger


class SicproDeckApi(models.TransientModel):
    _inherit = 'sicpro.modulo.deck.api'

    # Buscar todos los board
    def api_deck_board_buscar_todos(self, usuario):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards"
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
            return ("Deck API: La ejecución de la búsqueda de todos los BOARD ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # Buscar un board especifico
    def api_deck_board_buscar_id(self, usuario, board_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id)
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
            return ("Deck API: La ejecución de la búsqueda del BOARD específico ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # Crear board
    def api_deck_board_crear(self, usuario, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards"
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la creación del BOARD ha fallado, a continuación se muestran los datos:"
                    " %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # Modificar board
    def api_deck_board_modificar(self, usuario, board_id, payload):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id)
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("PUT", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la modificación del BOARD ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # Eliminar board
    def api_deck_board_eliminar(self, usuario, board_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id)
        payload = ""
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("DELETE", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))

            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la eliminación del BOARD ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)

    # Recuperar board eliminado
    def api_deck_board_recuperar(self, usuario, board_id):
        url_data = self.api_deck_url().url_data
        url = url_data + "/boards/" + str(board_id) + "/undo_delete"
        payload = ''
        headers = {'OCS-ApiRequest': 'true', 'Content-Type': 'application/json'}
        try:
            response = requests.request("POST", url, headers=headers, data=payload, verify=False,
                                        auth=(usuario.login, usuario.nube_token))
            if response.status_code == 200:
                data_json = response.json()
                for item in data_json:
                    return item
        except requests.HTTPError as e:
            return ("Deck API: La ejecución de la recuperación del BOARD ha fallado, a continuación se muestran"
                    " los datos: %r, msg: %r, content: %r", e.response.status_code, e.response.reason, e.response.content)
