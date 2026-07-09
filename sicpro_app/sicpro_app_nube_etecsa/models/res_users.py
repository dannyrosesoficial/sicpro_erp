# -*- coding: utf-8 -*-


import re
import requests
from odoo import models, fields, tools, _, api
from odoo.exceptions import ValidationError, UserError


class User(models.Model):
    _inherit = 'res.users'

    nube_token = fields.Char(string='Token de Acceso')
    nube_token_activo = fields.Boolean(string='Activar Token')

    @api.onchange('nube_token_activo')
    def onchange_nube_token_activo(self):
        if not self.nube_token_activo:
            usuario = self.env["res.users"].browse(self.env.user.id)
            for item in usuario:
                item.sudo().nube_token = None


class UserTokenNube(models.TransientModel):
    _name = 'sicpro.app.nube.etecsa.token'
    _description = 'Token de la Nube Etecsa'

    def _default_user_ids(self):
        usuario = self.env["res.users"].browse(self.env.user.id).login
        return usuario

    usuario = fields.Char(string='Usuario', required=True, default=_default_user_ids)
    password = fields.Char(string='Contraseña', required=True)

    def buscar_token(self):
        usuario = self.usuario
        password = self.password

        if usuario and password:
            url = "https://nube.etecsa.cu/ocs/v2.php/core/getapppassword"
            headers = {'OCS-ApiRequest': 'true'}
            payload = {}

            response = requests.request("GET", url, data=payload, headers=headers, verify=False,
                                        auth=(usuario, password), timeout=10)

            if response.status_code == 200:
                token = re.search('<apppassword>(.*?)</apppassword>', response.text).group(1)
                usuario = self.env["res.users"].browse(self.env.user.id)
                for item in usuario:
                    item.sudo().nube_token = token
                # redirecciono la salida
                return {'type': 'ir.actions.act_window_close'}
            else:
                raise UserError(
                    _("No son correctas las credenciales proporcionadas, no se pudo generar el TOKEN de acceso."))
        else:
            raise ValidationError(
                _("Es obligatorio introducir sus credenciales para generar el token de acceso a la Nube Etecsa."))
