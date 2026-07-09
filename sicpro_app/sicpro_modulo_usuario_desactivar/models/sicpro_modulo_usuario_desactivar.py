# -*- coding: utf-8 -*-


from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import models, fields, tools
from odoo.addons.sicpro_modulo_ldap_query.models.sicpro_modulo_ldap_registros import SicproLdapRegistros


class DesactivarUsuario(models.Model):
    _name = 'sicpro.app.modulo.usuario.desactivar'
    _description = 'Desactivación de los usuarios'

    name = fields.Boolean(string='Servicio', default=False)
    dias = fields.Integer(string='Días', required=False, default=0)
    company_id = fields.Many2one('res.company', string='Proceso', default=lambda self: self.env.company)
    tipo = fields.Selection(string='Tipo', required=True,
                            selection=[('acceso', 'Periodo de tiempo sin acceder al sistema.'),
                                       ('registro', 'Periodo de tiempo para validar el registro del sistema.'),
                                       ('ldap', 'Desactivar usuarios que no existe en LDAP.'), ], )
    avisos = fields.Many2many('sicpro.app.modulo.usuario.desactivar.dias', 'sicpro_modulo_desactivar_usuario_dias_rel',
                              string='Días de aviso')

    # actualizo la bitácora del usuario
    def actualizar_bitacora_desactivaciones(self, usuario, tipo):
        global movimiento, nota, rol, roles

        movimiento = 'desactivado'
        nota = 'El usuario fue archivado, pasando al estado de deshabilitado, ' \
               'fueron removidos todos los roles y permisos que tenía asignado.'
        # busco el rol de desactivación
        if tipo == 'ldap':
            rol = self.env['sicpro.modulo.roles'].sudo().search([('tipo_desactivar', '=', 'ldap')])
        elif tipo == 'registro':
            rol = self.env['sicpro.modulo.roles'].sudo().search([('tipo_desactivar', '=', 'registro')])
        elif tipo == 'acceso':
            rol = self.env['sicpro.modulo.roles'].sudo().search([('tipo_desactivar', '=', 'acceso')])
        roles = rol.ids
        bitacora_data = {'name': movimiento, 'usuario': usuario.id, 'roles': roles, 'nota': nota, }

        # creo el registro del usuario en la bitácora
        self.env['sicpro.app.soporte.bitacora'].create(bitacora_data)

    # Cron para desactivar el usuario si no existe o está desactivado en LDAP (No necesita enviar el correo de aviso)
    def cron_desactiva_usuarios_ldap(self):
        servicio = self.env['sicpro.app.modulo.usuario.desactivar'].search(
            ['&', ('tipo', '=', 'ldap'), ('name', '=', True)])
        # verífico el estado de activación del servicio
        if servicio:
            # busco los usuarios con permisos a recibir los correos alerta
            admin = self.env['res.users'].sudo().search(
                [('groups_id', 'in', self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])

            # Selecciono el usuario y los administradores
            notifica = ''
            for value in admin:
                notifica += str(value.partner_id.email_formatted)
            email_values = {'email_to': notifica, }

            # Busco el usuario para realizar la comparación.
            usuarios = self.env['res.users'].search(['&', ('active', '=', True), ('tipo_usuario', '=', 'ldap')])

            # verifico el usuario
            for item in usuarios:
                filtro = '(uid=' + item.login + ')'
                # realizo la solicitud de datos directamente al ldap empresarial
                data = SicproLdapRegistros.check_ldap_usuario(self, filtro)

                # verífico que exista el usuario para determinar su estado en LDAP
                if data:
                    estado = tools.ustr(data[0][1]['accountStatus'][0])
                else:
                    estado = 'noaccess'

                # verífico el estado del usuario en LDAP
                if data and estado == 'active':
                    print('El Usuario existe y está activo en LDAP')
                else:
                    # print('El Usuario no existe o no está activo en LDAP')
                    # creo el registro en la bitácora
                    bitacora_usuario = item
                    bitacora_tipo = 'ldap'
                    self.actualizar_bitacora_desactivaciones(bitacora_usuario, bitacora_tipo)
                    # desactivo al usuario
                    item.active = False
                    item.partner_id.active = False

                    # Envío el correo a los seguidores del registro
                    if item.user_inversionista:
                        local_context = item.env.context.copy()
                        template = item.env.ref(
                            'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_ldap_inversionistas')
                        template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)
                    else:
                        local_context = item.env.context.copy()
                        template = item.env.ref('sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_ldap')
                        template.with_context(local_context).send_mail(item.id, force_send=True, email_values=email_values)

            # verífico que los contactos esten en el mismo estado que los usuarios, paso a archivar el contacto
            contactos = self.env['res.users'].search(['|', ('active', '=', True), ('active', '=', False)])
            for contact in contactos:
                if contact.partner_id.active and not contact.active:
                    contact.partner_id.active = contact.active

            # envío el correo de aviso de la ejecución de la acción
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_modulo_usuario_desactivar.administracion_ejecucion_desactivacion_ldap')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
        else:
            print('SERVICIO DESACTIVADO')

    # Cron para desactivar el usuario sin entrar al sistema en el periodo de tiempo estipulado
    def cron_desactiva_usuarios_acceso(self):
        servicio = self.env['sicpro.app.modulo.usuario.desactivar'].search([('tipo', '=', 'acceso')])
        # verífico el estado de activación del servicio
        for data in servicio:
            if data.name and data.dias > 1:
                # busco los administradores con permisos a recibir los correos alerta
                admin = self.env['res.users'].sudo().search([('groups_id', 'in', self.env.ref(
                    'sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])

                # comienza la comprobación de fechas
                dias = data.dias
                fecha_limite = fields.Date.context_today(self) - relativedelta(days=dias)
                # Busco el usuario sin conectarse por un periodo de días.
                usuarios_desactivar = self.env['res.users'].search(
                    ['&', ('login_date', '<', fecha_limite), ('tipo_usuario', '=', 'ldap')])

                for item in usuarios_desactivar:
                    # creo el registro en la bitácora
                    bitacora_usuario = item
                    bitacora_tipo = 'acceso'
                    self.actualizar_bitacora_desactivaciones(bitacora_usuario, bitacora_tipo)
                    # Desactivo al usuario
                    item.active = False
                    item.partner_id.active = False

                    # Selecciono el usuario y los administradores
                    notifica = ''
                    for value in admin:
                        notifica += str(value.partner_id.email_formatted)
                    notifica += str(item.partner_id.email_formatted)

                    email_values = {'email_to': notifica, }
                    # Envío el correo a los seguidores del registro
                    if item.user_inversionista:
                        local_context = item.env.context.copy()
                        template = item.env.ref(
                            'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_acceso_inversionistas')
                        template.with_context(local_context).send_mail(
                            item.id, force_send=True, email_values=email_values)
                    else:
                        local_context = item.env.context.copy()
                        template = item.env.ref(
                            'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_acceso')
                        template.with_context(local_context).send_mail(
                            item.id, force_send=True, email_values=email_values)

                # comienza la comprobación de notificaciones de aviso
                for avisos in data.avisos:
                    fecha_aviso = fecha_limite - relativedelta(days=avisos.name)
                    fecha_aviso_inicial = datetime.combine(fecha_aviso, datetime.min.time())
                    fecha_aviso_final = datetime.combine(fecha_aviso, datetime.max.time())

                    # Busco el usuario en el periodo de días seleccionado.
                    usuarios_avisos = self.env['res.users'].search(
                        ['&', '&', ('login_date', '>', fecha_aviso_inicial), ('login_date', '<', fecha_aviso_final),
                         ('tipo_usuario', '=', 'ldap')])
                    # envío notificación al usuario
                    for user in usuarios_avisos:
                        email_values = {'email_to': user.partner_id.email_formatted, }
                        # Envío el correo a los seguidores del registro
                        if user.user_inversionista:
                            template = user.env.ref(
                                'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_acceso_inversionistas')
                            template.with_context(dias=avisos.name).send_mail(user.id, force_send=True,
                                                                              email_values=email_values)
                        else:
                            template = user.env.ref(
                                'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_acceso')
                            template.with_context(dias=avisos.name).send_mail(user.id, force_send=True,
                                                                              email_values=email_values)
            else:
                print('SERVICIO DESACTIVADO')

    # Cron para desactivar al usuario sin validar el registro de sistema en el periodo de tiempo estipulado
    def cron_desactiva_usuarios_registro(self):
        servicio = self.env['sicpro.app.modulo.usuario.desactivar'].search([('tipo', '=', 'registro')])
        # verífico el estado de activación del servicio
        for data in servicio:
            if data.name and data.dias > 1:
                # Busco los usuarios con permisos a recibir los correos de
                # alerta
                admin = self.env['res.users'].sudo().search([('groups_id', 'in', self.env.ref(
                    'sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])

                # comienza la comprobación de fechas
                dias = data.dias
                fecha_limite = fields.Date.context_today(self) - relativedelta(days=dias)
                # Busco el usuario sin conectarse por un periodo de días.
                usuarios = self.env['res.users'].search(
                    ['&', ('create_date', '<', fecha_limite), ('tipo_usuario', '=', 'ldap')])

                # mapeo los usuarios para determinar los que han iniciado sesión
                dic = []
                for user in usuarios:
                    dic.append({"id": user.id, "login_date": user.login_date,
                                "email_formatted": user.partner_id.email_formatted,})

                # verifico el tiempo de registro del usuario
                for item in dic:
                    if not item['login_date']:
                        # Selecciono el usuario y los administradores
                        notifica = ''
                        for value in admin:
                            notifica += str(value.partner_id.email_formatted)
                        notifica += str(item['email_formatted'])
                        email_values = {'email_to': notifica, }

                        # Desactivo y envío el correo a los seguidores del registro
                        user_mail = self.env['res.users'].search([('id', '=', item['id'])])
                        for mail in user_mail:
                            # creo el registro en la bitácora
                            bitacora_usuario = user_mail
                            bitacora_tipo = 'registro'
                            self.actualizar_bitacora_desactivaciones(bitacora_usuario, bitacora_tipo)
                            # desactivo al usuario
                            mail.active = False
                            mail.partner_id.active = False

                            if mail.user_inversionista:
                                local_context = mail.env.context.copy()
                                template = mail.env.ref(
                                    'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_registro_inversionistas')
                                template.with_context(local_context).send_mail(mail.id, force_send=True,
                                                                               email_values=email_values)
                            else:
                                local_context = mail.env.context.copy()
                                template = mail.env.ref(
                                    'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_registro')
                                template.with_context(local_context).send_mail(mail.id, force_send=True,
                                                                               email_values=email_values)

                # comienza la comprobación de notificaciones de aviso
                for avisos in data.avisos:
                    fecha_aviso = fecha_limite - relativedelta(days=avisos.name)
                    fecha_aviso_inicial = datetime.combine(fecha_aviso, datetime.min.time())
                    fecha_aviso_final = datetime.combine(fecha_aviso, datetime.max.time())

                    # Busco el usuario en el periodo de días seleccionado.
                    usuarios = self.env['res.users'].search(
                        ['&', '&', ('create_date', '>', fecha_aviso_inicial), ('create_date', '<', fecha_aviso_final),
                         ('tipo_usuario', '=', 'ldap')])

                    # mapeo los usuarios para determinar los que han iniciado sesión
                    dic = []
                    for user in usuarios:
                        dic.append({"id": user.id, "login_date": user.login_date,
                                    "email_formatted": user.partner_id.email_formatted, })

                    # verifico el tiempo de registro del usuario
                    for item in dic:
                        if not item['login_date']:
                            user = self.env['res.users'].search([('id', '=', item['id'])])
                            # envío notificación al usuario
                            email_values = {'email_to': user.partner_id.email_formatted, }
                            # Envío el correo a los seguidores del registro
                            if user.user_inversionista:
                                template = user.env.ref(
                                    'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_registro_inversionistas')
                                template.with_context(dias=avisos.name).send_mail(user.id, force_send=True,
                                                                                  email_values=email_values)
                            else:
                                template = user.env.ref(
                                    'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_registro')
                                template.with_context(dias=avisos.name).send_mail(user.id, force_send=True,
                                                                                  email_values=email_values)

            else:
                print('SERVICIO DESACTIVADO')
