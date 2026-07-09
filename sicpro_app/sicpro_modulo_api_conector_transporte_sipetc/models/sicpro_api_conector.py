# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import base64
from datetime import datetime
import requests
import urllib3
from odoo import models, fields
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError

# Desactiva específicamente la advertencia de peticiones HTTPS no verificadas
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiConector(models.Model):
    _inherit = 'sicpro.modulo.api.conector'

    name = fields.Selection(selection_add=[
        ('sicpro.app.transporte.sipetc', 'APLICACIÓN DE TRANSPORTE - SIPETC')],
                            ondelete={
                                'sicpro.app.transporte.sipetc': 'cascade'})

    # IMPORTANTE: El nombre de la acción debe ser 'api_test_' + el nombre del valor del campo name
    def conector_api_test_sicpro_app_transporte_sipetc(self):
        app = self.env['sicpro.modulo.api.conector'].sudo().search(
            [('name', '=', 'sicpro.app.transporte.sipetc')])
        usuario = app.usuario
        password = app.password
        url_login = app.url_login
        url_data = app.url_data

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
                # envío credenciales al url del data
                response = requests.get(url_data, headers=headerData,
                                        verify=False)
                if response.status_code == 200:
                    raise ValidationError('Conexión establecida con éxito.')
                else:
                    raise ValidationError(
                        "Conexión reusada en el url Data, Verifíquelo\n\n" + MSG_SOPORTE_SICPRO)
            else:
                raise ValidationError(
                    "Conexión reusada en el url Login, Verifíquelo\n\n" + MSG_SOPORTE_SICPRO)
        else:
            raise ValidationError(
                "Los campos de usuario o contraseña están vacíos, verifíquelo\n\n" + MSG_SOPORTE_SICPRO)

    # IMPORTANTE: El nombre de la acción debe ser 'api_cron_' + el nombre del valor del campo name
    def conector_api_cron_sicpro_app_transporte_sipetc(self):
        # compruebo que esté creada la configuración de la aplicación api
        app = self.env['sicpro.modulo.api.conector'].sudo().search(
            [('name', '=', 'sicpro.app.transporte.sipetc')])
        if app:
            app_id = app.app_id
            usuario = app.usuario
            password = app.password
            url_login = app.url_login
            url_data = app.url_data
            url_cierre = app.url_cierre
            fecha_inicio = datetime.today()
            registros_creados = 0
            registros_actualizados = 0
            registros_archivados = 0
            dic_equipos = []
            seguidores = self.env['res.users']

            # Busco los usuarios para el envío del correo de notificación de la ejecución.
            group_notif = self.env.ref(
                'sicpro_app_administracion.grupo_app_administracion_notificaciones',
                raise_if_not_found=False)
            if group_notif:
                seguidores = group_notif.user_ids


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
                # envío credenciales al url del data
                response = requests.get(url_data, headers=headerData,
                                        verify=False)

                if response.status_code == 200:
                    json = response.json()
                    # devuelvo arreglo de los equipos
                    equipos = json["equipos"]

                    # verífico los números de matrícula el que no exista lo archivo
                    # lleno el dic con los números de las matrículas de los vehículos
                    for item2 in equipos:
                        dic_equipos.append(item2['matricula'])
                    # realizo la comparación
                    todos_reg = self.env[
                        'sicpro.app.transporte.general'].sudo().search(
                        [('active', '=', True)])
                    for item1 in todos_reg:
                        estado = item1.matricula in dic_equipos
                        if not estado:
                            item1.active = False
                            # actualizo la cantidad de registros archivados
                            registros_archivados += 1

                    for item in equipos:
                        # verífico que exista el vehículo en el sicpro
                        data = self.env[
                            'sicpro.app.transporte.general'].sudo().search(
                            [('matricula', '=', item['matricula'])])

                        # Busco él, id del chofer por el carnet de identidad en la app de trabajadores
                        chofer_id = self.env['sicpro.app.trabajadores'].search(
                            [('identification_id', '=', item['choferCi'])]).id
                        # Busco él, id del jefe del chofer por el carnet de identidad
                        jefe_id = self.env['sicpro.app.trabajadores'].search([(
                                                                              'identification_id',
                                                                              '=',
                                                                              item[
                                                                                  'jefeChoferCi'])]).id

                        # Busco él id de la marca en los nomencladores del sicpro por el nombre de la marca según SIPETC
                        marca_id = self.env[
                            'sicpro.app.transporte.modelo'].search(
                            [('name', '=', item['marcaNombre'])]).id

                        if data.matricula:
                            # actualizo registros del transporte existente en sicpro desde el SIPE TC
                            data.sudo().write(
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
                                 'jefeChoferNombre': item['jefeChoferNombre'],
                                 'jefeChoferCi': item['jefeChoferCi'],
                                 'jefeChoferCargo': item['jefeChoferCargo'],
                                 'jefeChoferDireccion': item[
                                     'jefeChoferDireccion'],
                                 'jefeChoferLicencia': item[
                                     'jefeChoferLicencia'],
                                 'jefeChoferEsChoferProfesional': item[
                                     'jefeChoferEsChoferProfesional'],
                                 'parqueoNombre': item['parqueoNombre'],
                                 'parqueoDireccion': item['parqueoDireccion'],
                                 'parqueoTipo': item['parqueoTipo'],
                                 'parqueoProvincia': item['parqueoProvincia'],
                                 'capacidadCargaNombre': item[
                                     'capacidadCargaNombre'],
                                 'codigoEquipo': item['codigoEquipo'],
                                 'numeroCirculacion': item[
                                     'numeroCirculacion'],
                                 'numeroInventario': item['numeroInventario'],
                                 'fechaRecibo': item['fechaRecibo'],
                                 'annoFabricacion': item['annoFabricacion'],
                                 'vin': item['vin'],
                                 'numeroSerie': item['numeroSerie'],
                                 'numeroMotor': item['numeroMotor'],
                                 'marcaMotorNombre': item['marcaMotorNombre'],
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
                                 'name': item['choferNombre'] + ": " + item[
                                     'matricula'] + " " + item[
                                             'tipoNombre'] + " " + item[
                                             'marcaNombre'] + " " + item[
                                             'modeloNombre'],
                                 'fecha_actualizado': datetime.today(),
                                 'chofer_trabajador_id': chofer_id,
                                 'jefe_trabajador_id': jefe_id,
                                 'marca_id': marca_id, })
                            # actualizo la cantidad de registros actualizados
                            registros_actualizados += 1
                        else:
                            # creo registros del transporte por cada uno que existen en el SIPE TC
                            self.env[
                                'sicpro.app.transporte.general'].sudo().create(
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
                                 'matricula': item['matricula'],
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
                                 'jefeChoferNombre': item['jefeChoferNombre'],
                                 'jefeChoferCi': item['jefeChoferCi'],
                                 'jefeChoferCargo': item['jefeChoferCargo'],
                                 'jefeChoferDireccion': item[
                                     'jefeChoferDireccion'],
                                 'jefeChoferLicencia': item[
                                     'jefeChoferLicencia'],
                                 'jefeChoferEsChoferProfesional': item[
                                     'jefeChoferEsChoferProfesional'],
                                 'parqueoNombre': item['parqueoNombre'],
                                 'parqueoDireccion': item['parqueoDireccion'],
                                 'parqueoTipo': item['parqueoTipo'],
                                 'parqueoProvincia': item['parqueoProvincia'],
                                 'capacidadCargaNombre': item[
                                     'capacidadCargaNombre'],
                                 'codigoEquipo': item['codigoEquipo'],
                                 'numeroCirculacion': item[
                                     'numeroCirculacion'],
                                 'numeroInventario': item['numeroInventario'],
                                 'fechaRecibo': item['fechaRecibo'],
                                 'annoFabricacion': item['annoFabricacion'],
                                 'vin': item['vin'],
                                 'numeroSerie': item['numeroSerie'],
                                 'numeroMotor': item['numeroMotor'],
                                 'marcaMotorNombre': item['marcaMotorNombre'],
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
                                 'name': item['choferNombre'] + ": " + item[
                                     'matricula'] + " " + item[
                                             'tipoNombre'] + " " + item[
                                             'marcaNombre'] + " " + item[
                                             'modeloNombre'],
                                 'fecha_actualizado': datetime.today(),
                                 'chofer_trabajador_id': chofer_id,
                                 'jefe_trabajador_id': jefe_id,
                                 'marca_id': marca_id, })
                            # actualizo la cantidad de registros creados
                            registros_creados += 1

                # cierro la session en el sistema SIPE TC
                response = requests.get(url_cierre, headers=headerData,
                                        verify=False)

                # envío el correo electrónico
                for participante in seguidores:
                    email_values = {'email_to': participante.email_formatted, }
                    local_context = self.env.context.copy()
                    template = self.env.ref(
                        'sicpro_modulo_api_conector_transporte_sipetc.transporte_conector_rest_api_exito')
                    template.with_context(local_context).send_mail(app.id,
                                                                   force_send=True,
                                                                   email_values=email_values)

                # actualizo el historial de conexiones
                self.env['sicpro.modulo.api.conector.historial'].sudo().create(
                    {'name': 'APLICACIÓN DE TRANSPORTE', 'app_externa': app_id,
                     'fecha_inicio': fecha_inicio,
                     'fecha_fin': datetime.today(),
                     'registros_creados': registros_creados,
                     'registros_actualizados': registros_actualizados,
                     'registros_archivados': registros_archivados,
                     'estado': 'exito', })
                return data
            else:
                # envío el correo electrónico
                for participante in seguidores:
                    email_values = {'email_to': participante.email_formatted, }
                    local_context = self.env.context.copy()
                    template = self.env.ref(
                        'sicpro_modulo_api_conector_transporte_sipetc.transporte_conector_rest_api_fallida')
                    template.with_context(local_context).send_mail(app.id,
                                                                   force_send=True,
                                                                   email_values=email_values)

                # actualizo el historial de conexiones
                self.env['sicpro.modulo.api.conector.historial'].sudo().create(
                    {'name': 'APLICACIÓN DE TRANSPORTE', 'app_externa': app_id,
                     'fecha_inicio': datetime.today(),
                     'fecha_fin': datetime.today(), 'registros_creados': 0,
                     'registros_actualizados': 0, 'registros_archivados': 0,
                     'estado': 'fallido', })
        else:
            print(
                "No se ha configurado el servicio para la APLICACIÓN DE TRANSPORTE - app_id:siptc, "
                "no será ejecutado el cron: 'conector_api_cron_sicpro_app_transporte' ")
