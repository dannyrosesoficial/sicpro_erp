# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from datetime import datetime
from random import randint
from dateutil.relativedelta import relativedelta
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

def _default_color():
    return randint(1, 11)


class DesactivarUsuario(models.Model):
    _name = 'sicpro.app.modulo.usuario.desactivar'
    _description = 'Desactivación de los usuarios'

    name = fields.Boolean(string='Servicio', default=False)
    dias = fields.Integer(string='Días', required=False, default=0)
    company_id = fields.Many2one('res.company', string='Proceso',
                                 default=lambda self: self.env.company)
    tipo = fields.Selection(string='Tipo', required=True, selection=[
        ('acceso', 'Periodo de tiempo sin acceder al sistema.'), (
        'registro', 'Periodo de tiempo para validar el registro del sistema.'),
        ('ldap', 'Desactivar usuarios que no existe en LDAP.'), ])
    avisos = fields.Many2many('sicpro.app.modulo.usuario.desactivar.dias',
                              'sicpro_modulo_desactivar_usuario_dias_rel',
                              string='Días de aviso')
    color = fields.Integer(string='Color',
                           default=lambda self: _default_color())
    # Campo para los usuarios exceptuados de la desactivación
    usuario_excepcion_ids = fields.Many2many('res.users',
        'rel_desactivar_usuarios_excepcion',
        'desactivar_id', 'user_id', string='Usuarios Exceptuados',
        help="Los usuarios seleccionados aquí no serán desactivados por ningún CRON.")

    # actualizo la bitácora del usuario

    def actualizar_bitacora_desactivaciones(self, usuario, tipo):
        movimiento = 'desactivado'
        nota = (
            'El usuario fue archivado, pasando al estado de deshabilitado, '
            'fueron removidos todos los roles y permisos que tenía asignado.')

        # Búsqueda dinámica y optimizada del rol (limit=1 por seguridad)
        rol = self.env['res.users.role'].sudo().search(
            [('tipo_desactivar', '=', tipo)], limit=1)

        # Formato correcto para relaciones Many2many en Odoo: (6, 0, [lista_de_ids])
        roles_formato = [(6, 0, rol.ids)] if rol else []

        # Preparar el diccionario de datos con el nuevo campo
        bitacora_data = {
            'name': movimiento, 'usuario': usuario.id,
            'roles': roles_formato, 'nota': nota,
            'tipo_desactivacion': tipo,
            'fecha': fields.Datetime.now(),
        }

        self.env['sicpro.app.soporte.bitacora'].sudo().create(bitacora_data)

        # Remover los roles reales del usuario en el sistema
        if usuario.role_ids:
            usuario.sudo().write({'role_ids': [(5, 0, 0)]})

    # Cron para desactivar el usuario si no existe o está desactivado en LDAP
    # (No necesita enviar el correo de aviso)
    def cron_desactiva_usuarios_ldap(self):
        # 1. Verificación del estado de activación del servicio
        servicio = self.env['sicpro.app.modulo.usuario.desactivar'].search(
            [('tipo', '=', 'ldap'), ('name', '=', True)], limit=1)

        if not servicio:
            _logger.info('SICPRO: SERVICIO DE DESACTIVACIÓN LDAP DESACTIVADO')
            return

        # --- PROTECCIÓN: Lista Blanca + Admin ---
        # Obtenemos los IDs de la lista blanca y aseguramos que el ID 1 y 2 (
        # Admin) nunca sea procesado
        ignore_ids = servicio.usuario_excepcion_ids.ids + [1] + [2]

        # 2. Obtener administradores para notificaciones (Configuración de SICPRO)
        admin = self.env['res.users']
        group_notif = self.env.ref(
            'sicpro_app_administracion.grupo_app_administracion_notificaciones',
            raise_if_not_found=False)

        if group_notif:
            admin = group_notif.user_ids

        # Preparar lista de correos de los administradores
        emails = [u.partner_id.email_formatted for u in admin if
                  u.partner_id.email]
        notifica = ','.join(emails)
        email_values = {'email_to': notifica}

        # 3. Buscar usuarios LDAP activos en SICPRO excluyendo a los protegidos
        usuarios = self.env['res.users'].search(
            [('active', '=', True), ('tipo_usuario', '=', 'ldap'),
                ('id', 'not in', ignore_ids)])

        # Instanciamos el modelo de conexión LDAP de SICPRO
        modelo_ldap = self.env['sicpro.app.modulo.ldap.registros']

        for item in usuarios:
            filtro = f'(uid={item.login})'
            # Consulta al servidor LDAP
            data = modelo_ldap.check_ldap_usuario(filtro)

            estado_ldap = 'noaccess'
            if data:
                # Decodificación de atributos para Odoo 19 / Python 3.11
                val_raw = data[0][1].get('accountStatus', [b'noaccess'])[0]
                estado_ldap = val_raw.decode('utf-8') if isinstance(val_raw,
                                                                    bytes) else str(
                    val_raw)

            # 4. Si el usuario no existe en LDAP o su estado no es 'active', desactivamos en SICPRO
            if not data or estado_ldap != 'active':
                # Actualizar bitácora registrando la causa 'ldap'
                self.actualizar_bitacora_desactivaciones(item, 'ldap')

                # Desactivación atómica del usuario y su ficha de contacto
                item.active = False
                if item.partner_id:
                    item.partner_id.active = False

                # Determinar la plantilla de correo según el perfil del usuario
                xml_id = 'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_ldap'
                if hasattr(item,
                           'user_inversionista') and item.user_inversionista:
                    xml_id = 'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_ldap_inversionistas'

                template_user = self.env.ref(xml_id, raise_if_not_found=False)
                if template_user:
                    template_user.send_mail(item.id, force_send=True,
                                            email_values=email_values)

        # 5. Envío del correo de aviso de finalización de la tarea automática
        template_fin = self.env.ref(
            'sicpro_modulo_usuario_desactivar.administracion_ejecucion_desactivacion_ldap',
            raise_if_not_found=False)

        if template_fin:
            template_fin.send_mail(self.id, force_send=True,
                                   email_values=email_values)

    # Cron para desactivar el usuario sin entrar al sistema en el periodo de
    # tiempo estipulado (Enviá el correo de aviso)
    def cron_desactiva_usuarios_acceso(self):
        # Busco la configuración del servicio de desactivación por acceso
        servicio = self.env['sicpro.app.modulo.usuario.desactivar'].search(
            [('tipo', '=', 'acceso')])

        for data in servicio:
            if data.name and data.dias > 1:
                # --- PROTECCIÓN: Lista Blanca + Admin ---
                # Extraemos IDs exceptuados y aseguramos el ID 1 y 2 (Admin)
                ignore_ids = data.usuario_excepcion_ids.ids + [1] + [2]

                # 1. Obtener administradores para notificaciones
                admin = self.env['res.users']
                group_notif = self.env.ref(
                    'sicpro_app_administracion.grupo_app_administracion_notificaciones',
                    raise_if_not_found=False)

                if group_notif:
                    admin = group_notif.user_ids

                # Preparar lista de correos de admin
                emails_admin = [u.partner_id.email_formatted for u in admin if
                                u.partner_id.email]

                # 2. Comprobación de fechas para desactivación real
                dias_limite = data.dias
                fecha_hoy = fields.Date.context_today(self)
                fecha_limite = fecha_hoy - relativedelta(days=dias_limite)

                # Busco usuarios LDAP activos que NO estén en la lista de ignorados
                usuarios_desactivar = self.env['res.users'].search(
                    [('login_date', '<', fecha_limite),
                        ('tipo_usuario', '=', 'ldap'), ('active', '=', True),
                        ('id', 'not in', ignore_ids)
                        # Aplicación de la protección
                    ])

                for item in usuarios_desactivar:
                    # Actualizar bitácora con el tipo 'acceso'
                    self.actualizar_bitacora_desactivaciones(item, 'acceso')

                    # Desactivar usuario y su contacto de forma atómica
                    item.active = False
                    if item.partner_id:
                        item.partner_id.active = False

                    # Notificar a admins y al usuario afectado
                    destinatarios = emails_admin.copy()
                    if item.partner_id.email:
                        destinatarios.append(item.partner_id.email_formatted)

                    email_values = {'email_to': ','.join(destinatarios)}

                    # Plantilla según tipo de usuario (Inversionista o Estándar)
                    xml_id = 'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_acceso'
                    if hasattr(item,
                               'user_inversionista') and item.user_inversionista:
                        xml_id = 'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_acceso_inversionistas'

                    template = self.env.ref(xml_id, raise_if_not_found=False)
                    if template:
                        template.send_mail(item.id, force_send=True,
                                           email_values=email_values)

                # 3. Comprobación de notificaciones de AVISO (Preventivos)
                # Aquí recorremos la configuración de avisos configurada en el O2M/M2M
                for avisos in data.avisos:
                    # Calculamos el día exacto en que el usuario cumple el tiempo para ser avisado
                    # Ejemplo: Límite 30 días, aviso a los 5 días restantes -> login_date hace 25 días
                    dia_aviso = fecha_hoy - relativedelta(
                        days=(dias_limite - avisos.name))

                    # Definir rango de tiempo para cubrir todo el día del aviso
                    inicio_dia = datetime.combine(dia_aviso,
                                                  datetime.min.time())
                    fin_dia = datetime.combine(dia_aviso, datetime.max.time())

                    # Buscamos usuarios que entraron por última vez en ese rango específico
                    usuarios_avisos = self.env['res.users'].search(
                        [('login_date', '>=', inicio_dia),
                            ('login_date', '<=', fin_dia),
                            ('tipo_usuario', '=', 'ldap'),
                            ('active', '=', True), ('id', 'not in', ignore_ids)
                            # También protegemos a los exceptuados de recibir avisos
                        ])

                    for user in usuarios_avisos:
                        email_values_aviso = {
                            'email_to': user.partner_id.email_formatted}

                        xml_id_aviso = 'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_acceso'
                        if hasattr(user,
                                   'user_inversionista') and user.user_inversionista:
                            xml_id_aviso = 'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_acceso_inversionistas'

                        template_aviso = self.env.ref(xml_id_aviso,
                                                      raise_if_not_found=False)
                        if template_aviso:
                            # Pasamos 'dias' al contexto para que la plantilla diga: "Tu cuenta se cerrará en X días"
                            template_aviso.with_context(
                                dias=avisos.name).send_mail(user.id,
                                force_send=True,
                                email_values=email_values_aviso)
            else:
                _logger.info(
                    'SICPRO: SERVICIO DE DESACTIVACIÓN POR ACCESO NO CONFIGURADO O DESACTIVADO')

    # Cron para desactivar al usuario sin validar el registro de sistema en el
    # periodo de tiempo estipulado (Enviá el correo de aviso)
    def cron_desactiva_usuarios_registro(self):
        # Busco la configuración para desactivación por primer registro
        servicio = self.env['sicpro.app.modulo.usuario.desactivar'].search(
            [('tipo', '=', 'registro')])

        for data in servicio:
            if data.name and data.dias > 1:
                # --- PROTECCIÓN: Lista Blanca + Admin ---
                # Extraemos IDs de usuarios que jamás deben ser tocados
                ignore_ids = data.usuario_excepcion_ids.ids + [1] + [2]

                # 1. Obtener administradores para notificaciones (Corrección groups_id)
                admin = self.env['res.users']
                group_notif = self.env.ref(
                    'sicpro_app_administracion.grupo_app_administracion_notificaciones',
                    raise_if_not_found=False)

                if group_notif:
                    admin = group_notif.user_ids

                emails_admin = [u.partner_id.email_formatted for u in admin if
                                u.partner_id.email]

                # 2. Comprobación de fechas para desactivación definitiva
                dias_gracia = data.dias
                fecha_hoy = fields.Date.context_today(self)
                fecha_limite = fecha_hoy - relativedelta(days=dias_gracia)

                # Busco usuarios LDAP creados antes de la fecha límite que NUNCA han entrado
                # Excluimos explícitamente la lista ignore_ids
                usuarios_nunca_logueados = self.env['res.users'].search(
                    [('create_date', '<', fecha_limite),
                        ('login_date', '=', False),
                        ('tipo_usuario', '=', 'ldap'), ('active', '=', True),
                        ('id', 'not in', ignore_ids)])

                for user in usuarios_nunca_logueados:
                    # Actualizar bitácora con el tipo 'registro'
                    self.actualizar_bitacora_desactivaciones(user, 'registro')

                    # Desactivar usuario y partner de forma atómica
                    user.active = False
                    if user.partner_id:
                        user.partner_id.active = False

                    # Preparar destinatarios (Admins + Usuario afectado)
                    destinatarios = emails_admin.copy()
                    if user.partner_id.email:
                        destinatarios.append(user.partner_id.email_formatted)

                    email_values = {'email_to': ','.join(destinatarios)}

                    # Selección de plantilla según el tipo de perfil (Inversionista o General)
                    xml_id = 'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_registro'
                    if hasattr(user,
                               'user_inversionista') and user.user_inversionista:
                        xml_id = 'sicpro_modulo_usuario_desactivar.administracion_desactivar_usuario_registro_inversionistas'

                    template = self.env.ref(xml_id, raise_if_not_found=False)
                    if template:
                        template.send_mail(user.id, force_send=True,
                                           email_values=email_values)

                # 3. Comprobación de avisos preventivos (Recordatorios)
                for avisos in data.avisos:
                    # Calculamos el día que cumple el plazo para el aviso
                    # Si se desactiva a los 10 días y el aviso es "faltan 2", buscamos creados hace 8 días
                    dia_aviso = fecha_hoy - relativedelta(
                        days=(dias_gracia - avisos.name))

                    inicio_dia = datetime.combine(dia_aviso,
                                                  datetime.min.time())
                    fin_dia = datetime.combine(dia_aviso, datetime.max.time())

                    # Usuarios creados en ese rango de 24h que siguen sin entrar al sistema
                    usuarios_avisos = self.env['res.users'].search(
                        [('create_date', '>=', inicio_dia),
                            ('create_date', '<=', fin_dia),
                            ('login_date', '=', False),
                            ('tipo_usuario', '=', 'ldap'),
                            ('active', '=', True),
                            ('id', 'not in', ignore_ids)])

                    for u_aviso in usuarios_avisos:
                        email_val_aviso = {
                            'email_to': u_aviso.partner_id.email_formatted}

                        xml_id_aviso = 'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_registro'
                        if hasattr(u_aviso,
                                   'user_inversionista') and u_aviso.user_inversionista:
                            xml_id_aviso = 'sicpro_modulo_usuario_desactivar.administracion_aviso_desactivar_usuario_registro_inversionistas'

                        template_aviso = self.env.ref(xml_id_aviso,
                                                      raise_if_not_found=False)
                        if template_aviso:
                            # Pasamos los días restantes al contexto para la redacción del correo
                            template_aviso.with_context(
                                dias=avisos.name).send_mail(u_aviso.id,
                                force_send=True, email_values=email_val_aviso)
            else:
                _logger.info(
                    'SICPRO: SERVICIO DE DESACTIVACIÓN POR REGISTRO NO CONFIGURADO O DESACTIVADO')
