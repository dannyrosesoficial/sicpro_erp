# -*- coding: utf-8 -*-


import logging
from odoo.tools.pycompat import to_text
import ldap
from odoo import models, fields, tools

_logger = logging.getLogger(__name__)


class SicproLdapRegistros(models.Model):
    _name = 'sicpro.app.modulo.ldap.registros'
    _description = 'Registros del Servicio LDAP'
    _rec_name = 'employeeNumber'

    cn = fields.Char(string='Nombre')
    departmentNumber = fields.Char(string='Departamento')
    accountStatus = fields.Char(string='Estado')
    uid = fields.Char(string='Usuario')
    employeeType = fields.Char(string='Tipo Usuario')
    employeeNumber = fields.Char(string='Número Personal')
    ou = fields.Char(string='Unidad Organizativa')
    telephoneNumber = fields.Char(string='Teléfono Fijo')
    mobile = fields.Char(string='Teléfono Móvil')
    servicio = fields.Char(string='Servicios')
    ipnavegacion = fields.Char(string='IP Asignada')
    mail = fields.Char(string='Correo')
    title = fields.Char(string='Cargo')
    active = fields.Boolean(string='Active', default=True, required=False)

    # realiza las solicitudes de datos al ldap
    def check_ldap_usuario(self, filtro):
        Ldap_server = self.env['res.company.ldap']
        for conf in Ldap_server._get_ldap_dicts():
            conectar_ldap = Ldap_server._connect(conf)

            base_dn = conf["ldap_base"]
            uid = conf["ldap_binddn"]
            pwd = conf["ldap_password"]
            scope = ldap.SCOPE_SUBTREE
            retrieve_attributes = None
            filtro = "(&(objectClass=inetOrgPerson)" + filtro + ")"

            try:
                conectar_ldap.simple_bind_s(to_text(uid), to_text(pwd))
                l_search = conectar_ldap.search(base_dn, scope, filtro, retrieve_attributes)
                result_status, result_data = conectar_ldap.result(l_search)
                return result_data
            except ldap.LDAPError as e:
                print(e)

    # Cron para registrar en base de datos los usuarios que está en LDAP
    def cron_registrar_usuarios_ldap(self):
        # parámetros del historial de registros
        dic_uo = []
        reg_creados = 0
        reg_actualizados = 0
        reg_archivados = 0
        # busco los usuarios con permisos a recibir los correos alerta
        admin = self.env['res.users'].sudo().search(
            [('groups_id', 'in', self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])
        # Selecciono los administradores
        notifica = ''
        for value in admin:
            notifica += str(value.partner_id.email_formatted)
        email_values = {'email_to': notifica, }

        # Busco las unidades organizativas
        uo = self.env['sicpro.nomenclador.territorios'].search([('active', '=', True)])

        try:
            # verifico la unidad organizativa
            for item in uo:
                dic_uo.append(item.abreviatura)
                filtro = '(ou=' + item.abreviatura + ')(accountStatus=active)(!(employeeNumber=00000000))'
                data = self.check_ldap_usuario(filtro)

                # archivo los usuarios que ya no están en el ldap empresarial
                dic_ldap = []
                # Busco los usuarios en el registro pertenecientes a la misma UO
                todos_reg = self.env['sicpro.app.modulo.ldap.registros'].sudo().search(
                    ['&', ('active', '=', True), ('ou', '=', item.abreviatura)])
                # lleno el dic con los números de plaza para comparar de la UO específicas
                for item2 in data:
                    if 'employeeNumber' in item2[1]:
                        dic_ldap.append(tools.ustr(item2[1]['employeeNumber'][0]))
                # realizo la comparación de los números de plaza el que no exista lo archivo
                for item1 in todos_reg:
                    estado = item1.employeeNumber in dic_ldap
                    if not estado:
                        item1.active = False
                        reg_archivados += 1

                # verífico que exista la unidad organizativa en LDAP
                if data:
                    for value in data:
                        # comprobar la existencia de los key en la tupla
                        uid = tools.ustr(value[1]['uid'][0])
                        cn = tools.ustr(value[1]['cn'][0])
                        accountStatus = tools.ustr(value[1]['accountStatus'][0])
                        ou = tools.ustr(value[1]['ou'][0])

                        if 'employeeNumber' in value[1]:
                            employeeNumber = tools.ustr(value[1]['employeeNumber'][0])
                        else:
                            employeeNumber = False

                        if 'mail' in value[1]:
                            mail = tools.ustr(value[1]['mail'][0])
                        else:
                            mail = '-'

                        if 'servicio' in value[1]:
                            servicio = tools.ustr(value[1]['servicio'][0])
                        else:
                            servicio = '-'

                        if 'employeeType' in value[1]:
                            employeeType = tools.ustr(value[1]['employeeType'][0])
                        else:
                            employeeType = '-'

                        if 'title' in value[1]:
                            title = tools.ustr(value[1]['title'][0])
                        else:
                            title = '-'

                        if 'departmentNumber' in value[1]:
                            departmentNumber = tools.ustr(value[1]['departmentNumber'][0])
                        else:
                            departmentNumber = '-'

                        if 'telephoneNumber' in value[1]:
                            telephoneNumber = tools.ustr(value[1]['telephoneNumber'][0])
                        else:
                            telephoneNumber = '-'

                        if 'mobile' in value[1]:
                            mobile = tools.ustr(value[1]['mobile'][0])
                        else:
                            mobile = '-'

                        if 'ipnavegacion' in value[1]:
                            ipnavegacion = tools.ustr(value[1]['ipnavegacion'][0])
                        else:
                            ipnavegacion = '-'

                        # verífico que exista el usuario ldap en los contactos del sicpro
                        reg = self.env['sicpro.app.modulo.ldap.registros'].sudo().search([('uid', '=', uid)])

                        # verífico que exista el campo del número de trabajador
                        if employeeNumber:
                            if reg.uid:
                                # actualizo registros del contacto ldap
                                reg.sudo().write(
                                    {'cn': cn, 'accountStatus': accountStatus, 'mobile': mobile,
                                     'employeeType': employeeType, 'ou': ou, 'employeeNumber': employeeNumber,
                                     'servicio': servicio, 'mail': mail, 'title': title, 'ipnavegacion': ipnavegacion,
                                     'departmentNumber': departmentNumber, 'telephoneNumber': telephoneNumber,
                                     })
                                reg_actualizados += 1
                            else:
                                self.env[
                                    'sicpro.app.modulo.ldap.registros'].sudo().create(
                                    {'uid': uid, 'cn': cn, 'accountStatus': accountStatus, 'mobile': mobile,
                                     'employeeType': employeeType, 'ou': ou, 'employeeNumber': employeeNumber,
                                     'servicio': servicio, 'mail': mail, 'title': title, 'ipnavegacion': ipnavegacion,
                                     'departmentNumber': departmentNumber, 'telephoneNumber': telephoneNumber,
                                     })
                                reg_creados += 1

            # actualizo el historial de registros LDAP
            self.env['sicpro.app.modulo.ldap.historial'].sudo().create(
                {'name': dic_uo,
                 'fecha': fields.Datetime.now(),
                 'registros_creados': reg_creados,
                 'registros_actualizados': reg_actualizados,
                 'registros_archivados': reg_archivados,
                 'estado': 'exito', })

            template = self.env.ref('sicpro_modulo_ldap_query.plantilla_ldap_registros_query_ldap_correcto')
            template.with_context(nombre=dic_uo, fecha=fields.Datetime.now(), creados=reg_creados,
                                  actualizados=reg_actualizados, archivados=reg_archivados).send_mail(
                self.id, force_send=True, email_values=email_values)

        except Exception as e:
            _logger.exception(e)
            # print(e)
            # actualizo el historial de conexiones
            self.env[
                'sicpro.app.modulo.ldap.historial'].sudo().create(
                {'name': dic_uo,
                 'fecha': fields.Datetime.now(),
                 'registros_creados': reg_creados,
                 'registros_actualizados': reg_actualizados,
                 'registros_archivados': reg_archivados,
                 'estado': 'fallido',
                 })

            template = self.env.ref(
                'sicpro_modulo_ldap_query.plantilla_ldap_registros_query_ldap_fallido')
            template.with_context(nombre=dic_uo, fecha=fields.Datetime.now(), creados=reg_creados,
                                  actualizados=reg_actualizados, archivados=reg_archivados).send_mail(
                self.id, force_send=True, email_values=email_values)

