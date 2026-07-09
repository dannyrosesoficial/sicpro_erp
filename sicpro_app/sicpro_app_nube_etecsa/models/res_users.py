# -*- coding: utf-8 -*-


from odoo import api, fields, models
import requests
import base64
from odoo.exceptions import UserError
from odoo import models, fields, api, http, _


class Users(models.Model):
    _inherit = 'res.users'

    pass_secret = fields.Char(string='Pass_secret', required=False)

    # conexión con el sistema nube etecsa
    def api_conexion_nube_etecsa(self, ):
        #data = self.env['res.users'].sudo().search([('id', '=', uid)])
        usuario = 'daniel.borrero'
        password = 'Rosario.37.'
        url_login = 'https://nube.etecsa.cu/login'

        if usuario and password:
            # convierto credenciales a base64
            data = usuario + ":" + password
            base64Credencial = base64.b64encode(data.encode("utf-8")).decode(
                "utf-8")

            # encabezado del login y envío credenciales al login
            #headerLogin = {'Authorization': 'Basic' + base64Credencial}
            #response = requests.get(url_login, headers=headerLogin, verify=False)

            values = {'user': 'daniel.borrero',
                      'password': 'Rosario.37.'}

            response = requests.post(url='https://nube.etecsa.cu/login/', data=values, verify=False)


            print(response.content)

            if response.status_code == 200:
                raise UserError(_('Conexión establecida con éxito.'))
            else:
                raise UserError(_('Conexión reusada en el url Login, '
                                  'Verifíquelo'))
        else:
            raise UserError(_('Los campos de usuario o contraseña están '
                              'vacíos, verifíquelo'))