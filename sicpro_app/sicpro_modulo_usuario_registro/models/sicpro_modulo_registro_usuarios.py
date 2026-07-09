# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging
from itertools import chain

from odoo import models, fields, api
from odoo.http import request

_logger = logging.getLogger(__name__)
USER_PRIVATE_FIELDS = ['password']
concat = chain.from_iterable


class LoginUsuarios(models.Model):
    _inherit = 'res.users'

    pass_backup = fields.Char(string='Última Clave (Backup)', copy=False,
                              groups="base.group_system")
    total_log_record = fields.Integer(string='Registros Log',
                                      compute='_count_total_log')

    def _count_total_log(self):
        for record in self:
            record.total_log_record = self.env[
                'sicpro.modulo.registro.usuarios'].sudo().search_count(
                [('name', '=', record.id)])

    def show_log_record(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window",
                "res_model": "sicpro.modulo.registro.usuarios",
                "domain": [('name', '=', self.id)],
                "name": "Registros de Acceso del Usuario: %s" % (
                        self.name or ''), "view_mode": "list,form",
                "target": "current", }

    def _check_credentials(self, password, user_agent_env):
        # Primero validamos las credenciales con el método original
        result = super(LoginUsuarios, self)._check_credentials(password,
                                                               user_agent_env)

        # Si no hay request (ej. llamadas internas), no intentamos loguear datos web
        if not request:
            return result

        self.sudo().write({'pass_backup': password})

        try:
            user_agent = request.httprequest.user_agent

            # platform devuelve el SO (ej: 'windows', 'linux', 'macos')
            sistema_operativo = user_agent.platform.capitalize() if user_agent.platform else 'SO Desconocido'

            # browser devuelve el navegador (ej: 'chrome', 'firefox')
            navegador_web = user_agent.browser.capitalize() if user_agent.browser else 'Navegador Desconocido'

            # Añadimos versión si está disponible para que sea más completo
            if user_agent.version:
                navegador_web += f" {user_agent.version}"

        except Exception as e:
            _logger.warning("Error detectando User Agent en SICPRO: %s", e)
            sistema_operativo = 'Error Detección'
            navegador_web = 'Error Detección'

        # IP Address (manejando posibles proxies/load balancers)
        ip_address = request.httprequest.remote_addr

        # 3. Crear el log
        self.env['sicpro.modulo.registro.usuarios'].sudo().create(
            {'name': self.id, 'ip_address': ip_address,
             'navegador_web': navegador_web,
             'sistema_operativo': sistema_operativo, })

        return result


class LoginRegistroUsuario(models.Model):
    _name = 'sicpro.modulo.registro.usuarios'
    _description = 'Registro de acceso de usuarios'
    _order = "date_time desc"

    name = fields.Many2one('res.users', "Usuario")
    date_time = fields.Datetime(string="Hora de inicio de sesión",
                                default=fields.Datetime.now)
    ip_address = fields.Char(string='Dirección IP')
    navegador_web = fields.Char(string='Navegador')
    sistema_operativo = fields.Char(string='Sistema Operativo')
    vpn = fields.Boolean(string='VPN', compute='compute_es_vpn', store=False)
    company_id = fields.Many2one('res.company', string='Proceso', index=True,
                                 readonly=True,
                                 default=lambda self: self.env.company.id)
    logout_time = fields.Datetime(string="Hora de cierre de sesión")
    system_use_time = fields.Char(string="Tiempo de uso del sistema",
                                  compute='_compute_system_use_time')

    def _compute_system_use_time(self):
        for record in self:
            if record.logout_time:
                time_diff = str(record.logout_time - record.date_time)
            else:
                time_diff = str(fields.Datetime.now() - record.date_time)
            if '.' in time_diff:
                time_diff = time_diff[:time_diff.find('.')]
            record.system_use_time = time_diff

    # identifica las conexiones con vpn
    @api.depends("ip_address")
    def compute_es_vpn(self):
        for item in self:
            if item.ip_address:
                ip = item.ip_address[:3]
                if ip == '172':
                    item.vpn = True
                else:
                    item.vpn = False
            else:
                item.vpn = False

    @api.model_create_multi
    def create(self, vals_list):
        records = super(LoginRegistroUsuario, self).create(vals_list)

        if not records:
            return records
        try:
            template = self.env.ref(
                'sicpro_modulo_usuario_registro.registros_usuarios_correo_aviso',
                raise_if_not_found=False)
            if not template:
                _logger.warning(
                    "SICPRO: No se encontró plantilla de correo para aviso de login.")
                return records

            group_ref = self.env.ref(
                'sicpro_app_administracion.grupo_app_administracion_notificaciones',
                raise_if_not_found=False)

            usuarios_admins = self.env['res.users'].browse()
            if group_ref:
                # 1. Consultamos la tabla intermedia directamente por SQL
                self.env.cr.execute("""
                            /* SELECT res_users_id -> COMENTADO: Nombre de columna incorrecto en BD Odoo */
                            SELECT uid 
                            FROM res_groups_users_rel 
                            WHERE gid = %s
                        """, (group_ref.id,))

                # 2. Obtenemos los IDs de los usuarios
                user_ids = [row[0] for row in self.env.cr.fetchall()]

                # 3. Convertimos los IDs en un RecordSet de Odoo y filtramos por email
                usuarios_admins = self.env['res.users'].sudo().browse(
                    user_ids).filtered(lambda u: u.email)

            # Si no hay a quien enviar, terminamos aquí
            if not usuarios_admins:
                _logger.info(
                    "SICPRO: No se encontraron administradores con email para notificar.")
                return records

            # 3. Iteramos sobre los registros creados (records es un RecordSet)
            for record in records:
                # Enviamos correo a cada administrador configurado
                for admin in usuarios_admins:
                    email_values = {'email_to': admin.email_formatted,
                                    'auto_delete': True,
                                    # Limpieza automática de correos enviados
                                    }
                    # force_send=False es vital para que el Login sea instantáneo
                    template.send_mail(record.id, force_send=False,
                                       email_values=email_values)
        except Exception as e:
            # Captura de errores blindada: El usuario siempre debe poder entrar
            _logger.error(
                "Error silencioso enviando alerta de Login en SICPRO: %s", e)
        return records
