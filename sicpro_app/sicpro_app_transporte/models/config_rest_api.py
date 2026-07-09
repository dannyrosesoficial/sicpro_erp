# -*- coding: utf-8 -*-

import requests
import base64
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.http import request
from odoo import models, fields, api, http, _


class TransporteApi(models.Model):
    _name = 'sicpro.app.transporte.api'
    _order = "id asc"
    _description = 'Configuración Api del transporte SipeTC'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Aplicación', required=True)
    usuario = fields.Char('Usuario', required=False)
    password = fields.Char('Contraseña', required=False)
    web = fields.Char('Sitio Web', required=True)
    url_login = fields.Char('Url Login', required=True)
    url_data = fields.Char('Url Data', required=True)
    url_cierre = fields.Char('Url Cierre', required=True)
    descripcion = fields.Char('Descripción', required=False)
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)

    # prueba de conexión con el sistema externo
    def test_conexion_sipetc(self, ):
        data = self.env['sicpro.app.transporte.api'].sudo().search([('name', '=', 'SipeTC')])
        usuario = data.usuario
        password = data.password
        url_login = data.url_login
        url_data = data.url_data
        url_cierre = data.url_cierre

        if usuario and password:
            # convierto credenciales a base64
            data = usuario + ":" + password
            base64Credencial = base64.b64encode(data.encode("utf-8")).decode(
                "utf-8")

            # encabezado del login y envío credenciales al login
            headerLogin = {'Authorization': 'Basic' + base64Credencial}
            response = requests.get(url_login, headers=headerLogin,
                                    verify=False)

            if response.status_code == 200:
                # creo encabezado y token del url data
                json = response.json()
                authTokenValue = json["authToken"]
                headerData = {'Authorization': 'Basic' + base64Credencial,
                          'X-AUTH-TOKEN': authTokenValue}
                # envio credenciales al url del data
                response = requests.get(url_data, headers=headerData,
                                        verify=False)
                if response.status_code == 200:
                    raise UserError(_('Conexión establecida con éxito.'))
                else:
                    raise UserError(_('Conexión reusada en el url Data, '
                                  'Verifíquelo'))
            else:
                raise UserError(_('Conexión reusada en el url Login, '
                              'Verifíquelo'))
        else:
             raise UserError(_('Los campos de usuario o contraseña están '
                               'vacíos, verifíquelo'))

    def cron_ejecutar_sipetc(self, ):
        data_correo = self.env['sicpro.app.transporte.api'].sudo().search(
            [('name', '=', 'SipeTC')])
        usuario = data_correo.usuario
        password = data_correo.password
        url_login = data_correo.url_login
        url_data = data_correo.url_data
        url_cierre = data_correo.url_cierre

        # convierto credenciales a base64
        global data_equipos
        data = usuario + ":" + password
        base64Credencial = base64.b64encode(data.encode("utf-8")).decode(
            "utf-8")

        # encabezado del login y envio credenciales al login
        headerLogin = {'Authorization': 'Basic' + base64Credencial}
        response = requests.get(url_login, headers=headerLogin,
                                verify=False)

        if response.status_code == 200:
            # creo encabezado y token del url data
            json = response.json()
            authTokenValue = json["authToken"]
            headerData = {'Authorization': 'Basic' + base64Credencial,
                          'X-AUTH-TOKEN': authTokenValue}
            # envío credenciales al url del data
            response = requests.get(url_data, headers=headerData,
                                    verify=False)

            if response.status_code == 200:
                json = response.json()
                # devuelvo arreglo de los equipos
                equipos = json["equipos"]

                for item in equipos:
                    # verifico que exista el vehiculo en el sicpro
                    data = self.env[
                        'sicpro.app.transporte.general'].sudo().search([('matricula', '=', item['matricula'])])
                    data_equipos = ''

                    if data.matricula:
                        # actualizo registros del transporte existente en
                        # sicpro desde  el sipect
                        data_equipos = self.env['sicpro.app.transporte.general'].search([('matricula', '=', item['matricula'])])
                        data_equipos.sudo().write(
                            {'unidadNombre': item['unidadNombre'],
                                    'unidadAcronimo': item['unidadAcronimo'],
                                    'areaIdentificacion': item[
                                        'areaIdentificacion'],
                                    'areaNombre': item['areaNombre'],
                                    'grupoEquipoNombre': item[
                                        'grupoEquipoNombre'],
                                    'tipoNombre': item['tipoNombre'],
                                    'marcaNombre': item['marcaNombre'],
                                    'modeloNombre': item['modeloNombre'],
                                    'especialidadNombre': item[
                                        'especialidadNombre'],
                                    'actividadNombre': item['actividadNombre'],
                                    'actividadFundamentalNombre': item[
                                        'actividadFundamentalNombre'],
                                    'estadoTecnicoNombre': item[
                                        'estadoTecnicoNombre'],
                                    'color': item['color'],
                                    'combustibleNombre': item[
                                        'combustibleNombre'],
                                    'choferNombre': item['choferNombre'],
                                    'choferCi': item['choferCi'],
                                    'choferCargo': item['choferCargo'],
                                    'choferDireccion': item['choferDireccion'],
                                    'choferLicencia': item['choferLicencia'],
                                    'choferEsChoferProfesional': item[
                                        'choferEsChoferProfesional'],
                                    'jefeChoferNombre': item[
                                        'jefeChoferNombre'],
                                    'jefeChoferCi': item['jefeChoferCi'],
                                    'jefeChoferCargo': item['jefeChoferCargo'],
                                    'jefeChoferDireccion': item[
                                        'jefeChoferDireccion'],
                                    'jefeChoferLicencia': item[
                                        'jefeChoferLicencia'],
                                    'jefeChoferEsChoferProfesional': item[
                                        'jefeChoferEsChoferProfesional'],
                                    'parqueoNombre': item['parqueoNombre'],
                                    'parqueoDireccion': item[
                                        'parqueoDireccion'],
                                    'parqueoTipo': item['parqueoTipo'],
                                    'parqueoProvincia': item[
                                        'parqueoProvincia'],
                                    'capacidadCargaNombre': item[
                                        'capacidadCargaNombre'],
                                    'codigoEquipo': item['codigoEquipo'],
                                    'numeroCirculacion': item[
                                        'numeroCirculacion'],
                                    'numeroInventario': item[
                                        'numeroInventario'],
                                    'fechaRecibo': item['fechaRecibo'],
                                    'annoFabricacion': item['annoFabricacion'],
                                    'vin': item['vin'],
                                    'numeroSerie': item['numeroSerie'],
                                    'numeroMotor': item['numeroMotor'],
                                    'marcaMotorNombre': item[
                                        'marcaMotorNombre'],
                                    'modeloMotorNombre': item[
                                        'modeloMotorNombre'],
                                    'indiceConsumoNormado': item[
                                        'indiceConsumoNormado'],
                                    'indiceConsumoFabrica': item[
                                        'indiceConsumoFabrica'],
                                    'tieneOdometro': item['tieneOdometro'],
                                    'odometroOk': item['odometroOk'],
                                    'tieneHorametro': item['tieneHorametro'],
                                    'horametroOk': item['horametroOk'],
                                    'esAlquilado': item['esAlquilado'],
                                    'observacion': item['observacion'],
                                    'esParalizado': item['esParalizado'],
                                    'estaDefectuoso': item['estaDefectuoso'],
                                    'estaActivo': item['estaActivo'],
                                    'name': item['choferNombre'] + ": " +item['matricula'] + " " + item['tipoNombre'] + " " + item['marcaNombre'] + " " + item['modeloNombre'],
                             })
                    else:
                        # creo registros del transporte por cada uno que
                        # exisen el sipect
                        data_equipos = self.env['sicpro.app.transporte.general'].sudo().create(
                            {
                         'unidadNombre': item['unidadNombre'],
                         'unidadAcronimo': item['unidadAcronimo'],
                         'areaIdentificacion': item
                                    ['areaIdentificacion'],
                         'areaNombre': item['areaNombre'],
                         'grupoEquipoNombre': item['grupoEquipoNombre'],
                         'tipoNombre': item['tipoNombre'],
                         'marcaNombre': item['marcaNombre'],
                         'modeloNombre': item['modeloNombre'],
                         'matricula': item['matricula'],
                         'especialidadNombre': item
                                    ['especialidadNombre'],
                         'actividadNombre': item['actividadNombre'],
                         'actividadFundamentalNombre': item[
                             'actividadFundamentalNombre'],
                         'estadoTecnicoNombre': item
                                    ['estadoTecnicoNombre'],
                         'color': item['color'],
                         'combustibleNombre': item['combustibleNombre'],
                         'choferNombre': item['choferNombre'],
                         'choferCi': item['choferCi'],
                         'choferCargo': item['choferCargo'],
                         'choferDireccion': item['choferDireccion'],
                         'choferLicencia': item['choferLicencia'],
                         'choferEsChoferProfesional': item[
                             'choferEsChoferProfesional'],
                         'jefeChoferNombre': item['jefeChoferNombre'],
                         'jefeChoferCi': item['jefeChoferCi'],
                         'jefeChoferCargo': item['jefeChoferCargo'],
                         'jefeChoferDireccion': item
                                    ['jefeChoferDireccion'],
                         'jefeChoferLicencia': item
                                    ['jefeChoferLicencia'],
                         'jefeChoferEsChoferProfesional': item[
                             'jefeChoferEsChoferProfesional'],
                         'parqueoNombre': item['parqueoNombre'],
                         'parqueoDireccion': item['parqueoDireccion'],
                         'parqueoTipo': item['parqueoTipo'],
                         'parqueoProvincia': item['parqueoProvincia'],
                         'capacidadCargaNombre': item
                                    ['capacidadCargaNombre'],
                         'codigoEquipo': item['codigoEquipo'],
                         'numeroCirculacion': item['numeroCirculacion'],
                         'numeroInventario': item['numeroInventario'],
                         'fechaRecibo': item['fechaRecibo'],
                         'annoFabricacion': item['annoFabricacion'],
                         'vin': item['vin'],
                         'numeroSerie': item['numeroSerie'],
                         'numeroMotor': item['numeroMotor'],
                         'marcaMotorNombre': item['marcaMotorNombre'],
                         'modeloMotorNombre': item['modeloMotorNombre'],
                         'indiceConsumoNormado': item
                                    ['indiceConsumoNormado'],
                         'indiceConsumoFabrica': item
                                    ['indiceConsumoFabrica'],
                         'tieneOdometro': item['tieneOdometro'],
                         'odometroOk': item['odometroOk'],
                         'tieneHorametro': item['tieneHorametro'],
                         'horametroOk': item['horametroOk'],
                         'esAlquilado': item['esAlquilado'],
                         'observacion': item['observacion'],
                         'esParalizado': item['esParalizado'],
                         'estaDefectuoso': item['estaDefectuoso'],
                         'estaActivo': item['estaActivo'],
                         'name': item['choferNombre'] + ": " +item['matricula'] + " " + item['tipoNombre'] + " " + item['marcaNombre'] + " " + item['modeloNombre'],
                         })

            # cierro la session en el sistema sipetc
            response = requests.get(url_cierre, headers=headerData, verify=False)
            print(response.content)

            # Configuración para el envío del correo a la ejecución exitosa
            seguidores = self.env.ref(
                'sicpro_app_administracion.grupo_app_administracion_notificaciones').users
            # agrego los seguidores al modelo
            data_correo.message_subscribe(partner_ids=seguidores.partner_id.ids)
            # mantiene actualizado el correo de los seguidores del registro
            correos = ''
            for follower in data_correo.message_partner_ids:
                correos = str(correos) + str(follower.email_formatted)
            data_correo.correo_seguidores = correos
            # envío el correo a los seguidores del registro
            local_context = data_correo.env.context.copy()
            template = self.env.ref(
                'sicpro_app_transporte.transporte_actualizacion_sipe_exito')
            template.with_context(local_context).send_mail(data_correo.id,
                                                           force_send=True)
            return data_equipos
        else:
            # Configuración para el envío del correo a la ejecución fallida
            seguidores = self.env.ref(
                'sicpro_app_administracion.grupo_app_administracion_notificaciones').users
            # agrego los seguidores al modelo
            data_correo.message_subscribe(partner_ids=seguidores.partner_id.ids)
            # mantiene actualizado el correo de los seguidores del registro
            correos = ''
            for follower in data_correo.message_partner_ids:
                correos = str(correos) + str(follower.email_formatted)
            data_correo.correo_seguidores = correos
            # envío el correo a los seguidores del registro
            local_context = data_correo.env.context.copy()
            template = self.env.ref(
                'sicpro_app_transporte.transporte_actualizacion_sipe_fallida')
            template.with_context(local_context).send_mail(data_correo.id,
                                                           force_send=True)
