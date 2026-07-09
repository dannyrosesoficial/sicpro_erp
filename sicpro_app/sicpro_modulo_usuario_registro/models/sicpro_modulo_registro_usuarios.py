# -*- coding: utf-8 -*-


import logging
from itertools import chain

from odoo import models, fields, api
from odoo.http import request

try:
    import httpagentparser
except ImportError:
    pass

_logger = logging.getLogger(__name__)
USER_PRIVATE_FIELDS = ['password']
concat = chain.from_iterable


class LoginUsuarios(models.Model):
    _inherit = 'res.users'

    # campo para salvar el passuserbackup actual, la actualización se realiza desde el módulo de registro de usuarios
    pass_backup = fields.Char(string='PassBackup', required=False)
    total_log_record = fields.Integer('Registros Log', compute='_count_total_log')

    def _count_total_log(self):
        for record in self:
            record.total_log_record = self.env['sicpro.modulo.registro.usuarios'].sudo().search(
                [('name', '=', record.id)], count=True)

    def show_log_record(self):
        self.ensure_one()
        return {"type": "ir.actions.act_window", "res_model": "sicpro.modulo.registro.usuarios",
                "domain": [('name', '=', self.id)], "name": "Registros de Acceso del Usuario", 'view_mode': 'list',}

    @api.model
    def _check_credentials(self, password, user_agent_env):
        result = super(LoginUsuarios, self)._check_credentials(password, user_agent_env)
        agent = request.httprequest.environ.get('HTTP_USER_AGENT')
        agent_details = httpagentparser.detect(agent)
        # captura el passbackup
        self.sudo().pass_backup = password
        try:
            # Es necesario para errores al detectar sistemas operativos como android
            sistema_operativo = agent_details['os']['name']
        except:
            sistema_operativo = 'SO Móvil'

        navegador_web = agent_details['browser']['name']
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        vals = {
            'name': self.id,
            'ip_address': ip_address,
            'navegador_web': navegador_web,
            'sistema_operativo': sistema_operativo,
        }
        self.env['sicpro.modulo.registro.usuarios'].sudo().create(vals)

        return result


class LoginRegistroUsuario(models.Model):
    _name = 'sicpro.modulo.registro.usuarios'
    _description = 'Registro de acceso de usuarios'
    _order = "date_time desc"

    name = fields.Many2one('res.users', "Usuario")
    date_time = fields.Datetime(string="Hora de inicio de sesión", default=lambda self: fields.datetime.now())
    ip_address = fields.Char(string='Dirección IP')
    navegador_web = fields.Char(string='Navegador')
    sistema_operativo = fields.Char(string='Sistema Operativo')
    vpn = fields.Boolean(string='VPN', compute='compute_es_vpn', store=False)
    company_id = fields.Many2one('res.company', string='Proceso', index=True, readonly=True,
                                 default=lambda self: self.env.company.id)
    logout_time = fields.Datetime("Hora de cierre de sesión")
    system_use_time = fields.Char("Tiempo de uso del sistema", compute='_compute_system_use_time')

    def _compute_system_use_time(self):
        for record in self:
            if record.logout_time:
                time_diff = str(record.logout_time - record.date_time)
            else:
                time_diff = str(fields.Datetime.now() - record.date_time)
            time_diff = time_diff[:time_diff.find('.')]
            record.system_use_time = time_diff

    # identifica las conexiones con vpn
    @api.depends("ip_address")
    def compute_es_vpn(self):
        for item in self:
            ip = item.ip_address[:3]
            if ip == '172':
                item.vpn = True
            else:
                item.vpn = False

    @api.model
    def create(self, vals):
        res = super(LoginRegistroUsuario, self).create(vals)

        # busco los usuarios con permisos a recibir los correos de alerta
        usuarios = self.env['res.users'].sudo().search(
            [('groups_id', 'in', self.env.ref('sicpro_app_administracion.grupo_app_administracion_notificaciones').id)])

        for item in usuarios:
            # envío el correo electrónico
            email_values = {'email_to': item.email_formatted, }
            template = self.env.ref('sicpro_modulo_usuario_registro.registros_usuarios_correo_aviso')
            template.send_mail(res.id, force_send=True, email_values=email_values)

        return res
