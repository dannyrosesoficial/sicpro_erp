# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


import logging

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
    active = fields.Boolean(string='Active', default=True, required=False, index=True)

    # realiza las solicitudes de datos al ldap
    def check_ldap_usuario(self, filtro):
        Ldap_server = self.env['res.company.ldap']
        # Buscamos la configuración activa
        for conf in Ldap_server._get_ldap_dicts():
            # Usamos el método _connect que ya arreglamos para SSL
            conectar_ldap = Ldap_server._connect(conf)

            base_dn = conf["ldap_base"]
            uid = conf["ldap_binddn"]
            pwd = conf["ldap_password"]
            scope = ldap.SCOPE_SUBTREE

            # Construimos el filtro
            filtro_completo = "(&(objectClass=inetOrgPerson)" + filtro + ")"

            try:
                # 1. Autenticar el usuario de lectura (rouser)
                conectar_ldap.simple_bind_s(uid, pwd)

                # 2. Realizar la búsqueda directamente con search_st
                # LDAPWrapper.search_st devuelve directamente result_data
                # El 10 es el timeout en segundos
                result_data = conectar_ldap.search_st(base_dn, scope,
                    filtro_completo, timeout=10)

                return result_data

            except Exception as e:
                _logger.error("SICPRO: Error en la consulta LDAP: %s", e)
                return []

    def cron_registrar_trabajadores_ldap(self):
        # Parámetros del historial de registros
        dic_uo = []
        reg_creados = 0
        reg_actualizados = 0
        reg_archivados = 0

        # Inicializamos admin como un recordset vacío
        admin = self.env['res.users']

        # 1. Buscar usuarios para notificaciones
        group_notif = self.env.ref(
            'sicpro_app_administracion.grupo_app_administracion_notificaciones',
            raise_if_not_found=False)

        if group_notif:
            admin = group_notif.user_ids

        # Preparar correos de destino
        emails = [u.partner_id.email_formatted for u in admin if
                  u.partner_id.email]
        notifica = ','.join(emails)
        email_values = {'email_to': notifica}

        # 2. Buscar Unidades Organizativas (UO) activas
        unidades_org = self.env['sicpro.nomenclador.territorios'].search(
            [('active', '=', True)])

        try:
            for item in unidades_org:
                abreviatura = item.abreviatura
                dic_uo.append(abreviatura)

                # Construir filtro LDAP
                filtro = f'(&(ou={abreviatura})(accountStatus=active)(!(employeeNumber=00000000)))'
                data = self.check_ldap_usuario(filtro)

                if not data:
                    _logger.info(
                        "SICPRO: No se encontraron datos para la UO %s",
                        abreviatura)
                    continue

                # --- LÓGICA DE ARCHIVADO ---
                todos_reg_locales = self.search(
                    [('active', '=', True), ('ou', '=', abreviatura)])

                empleados_en_ldap = []
                for entry in data:
                    attrs = entry[1]
                    if 'employeeNumber' in attrs:
                        # Cambio: .decode() en lugar de tools.ustr()
                        val_raw = attrs['employeeNumber'][0]
                        empleados_en_ldap.append(
                            val_raw.decode('utf-8') if isinstance(val_raw,
                                                                  bytes) else str(
                                val_raw))

                for reg_local in todos_reg_locales:
                    if reg_local.employeeNumber not in empleados_en_ldap:
                        reg_local.active = False
                        reg_archivados += 1

                # --- LÓGICA DE CREACIÓN / ACTUALIZACIÓN (Ahora dentro del bucle de UO) ---
                for entry in data:
                    attrs = entry[1]
                    uid_raw = attrs.get('uid')
                    if not uid_raw:
                        continue

                    # Decodificación limpia para Odoo 19
                    uid = uid_raw[0].decode('utf-8') if isinstance(uid_raw[0],
                                                                   bytes) else str(
                        uid_raw[0])

                    def get_attr(name, default='-'):
                        val_list = attrs.get(name)
                        if not val_list:
                            return default
                        val = val_list[0]
                        return val.decode('utf-8') if isinstance(val,
                                                                 bytes) else str(
                            val)

                    employee_num_raw = attrs.get('employeeNumber')
                    if not employee_num_raw:
                        continue
                    emp_num = employee_num_raw[0].decode(
                        'utf-8') if isinstance(employee_num_raw[0],
                                               bytes) else str(
                        employee_num_raw[0])

                    vals = {'cn': get_attr('cn'),
                        'accountStatus': get_attr('accountStatus'),
                        'mobile': get_attr('mobile'),
                        'employeeType': get_attr('employeeType'),
                        'ou': get_attr('ou'), 'employeeNumber': emp_num,
                        'servicio': get_attr('servicio'),
                        'mail': get_attr('mail'), 'title': get_attr('title'),
                        'ipnavegacion': get_attr('ipnavegacion'),
                        'departmentNumber': get_attr('departmentNumber'),
                        'telephoneNumber': get_attr('telephoneNumber'), }

                    reg_existente = self.with_context(
                        active_test=False).sudo().search([('uid', '=', uid)],
                                                         limit=1)

                    if reg_existente:
                        if not reg_existente.active:
                            vals['active'] = True
                        reg_existente.write(vals)
                        reg_actualizados += 1
                    else:
                        vals['uid'] = uid
                        self.create(vals)
                        reg_creados += 1

            # 3. Registro en Historial de Éxito (Fuera del bucle for item in unidades_org)
            self.env['sicpro.app.modulo.ldap.historial'].sudo().create(
                {'name': str(dic_uo), 'fecha': fields.Datetime.now(),
                    'registros_creados': reg_creados,
                    'registros_actualizados': reg_actualizados,
                    'registros_archivados': reg_archivados,
                    'estado': 'exito', })

            template = self.env.ref(
                'sicpro_modulo_ldap_query.plantilla_ldap_registros_query_ldap_correcto',
                raise_if_not_found=False)
            if template:
                template.with_context(nombre=str(dic_uo),
                    fecha=fields.Datetime.now(), creados=reg_creados,
                    actualizados=reg_actualizados,
                    archivados=reg_archivados).send_mail(self.id,
                                                         force_send=True,
                                                         email_values=email_values)

        except Exception as e:
            _logger.exception("Error en CRON LDAP de SICPRO: %s", e)
            self.env['sicpro.app.modulo.ldap.historial'].sudo().create(
                {'name': str(dic_uo), 'fecha': fields.Datetime.now(),
                    'registros_creados': reg_creados,
                    'registros_actualizados': reg_actualizados,
                    'registros_archivados': reg_archivados,
                    'estado': 'fallido', })

            template_fallo = self.env.ref(
                'sicpro_modulo_ldap_query.plantilla_ldap_registros_query_ldap_fallido',
                raise_if_not_found=False)
            if template_fallo:
                template_fallo.with_context(nombre=str(dic_uo),
                    fecha=fields.Datetime.now(), creados=reg_creados,
                    actualizados=reg_actualizados,
                    archivados=reg_archivados).send_mail(self.id,
                                                         force_send=True,
                                                         email_values=email_values)