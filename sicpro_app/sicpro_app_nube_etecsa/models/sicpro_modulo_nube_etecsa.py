# -*- coding: utf-8 -*-


from odoo.exceptions import UserError
from odoo import models, fields, api, http, _
from odoo.http import dispatch_rpc, request
import webbrowser
import requests
import base64


class NubeEtecsa(models.TransientModel):
    _name = 'sicpro.modulo.nube.etecsa'
    _description = 'Modelo temporal Api Nube Etecsa'

    # conexión con el sistema nube etecsa
    def api_conexion_nube_etecsa(self, ):
        self.ensure_one()
        uid = self.env.uid
        usuarios = self.env['res.users'].search([('id', '=', uid)])
        if usuarios.login and usuarios.pass_backup:

            # url1 = 'https://nube.etecsa.cu/login'
            # curSession = request.Session()
            # payload = {'login': "usuario", 'password': "contraseña"}
            # curSession.post(url1, data=payload)
            # resp1 = requests.get(url1, data=payload, verify=False)
            # resp1 = requests.get(url1, verify=False)
            # url2 = 'https://nube.etecsa.cu/apps/files/'
            # curSession.get('https://nube.etecsa.cu/apps/files/')
            # resp2 = requests.post(url2, cookies=resp1.cookies, verify=False)
            # print(response.cookies)

            # url ='https://nube.etecsa.cu/login?user=daniel.borrero&password= '
            url = 'https://nube.etecsa.cu/'
            return url
        else:
            raise UserError(
                _('Su api de acceso no esta configurada, contacte al administrador'))
