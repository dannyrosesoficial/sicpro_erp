import logging
import subprocess
import sys

from odoo import models, fields, api

py_v = "python%s.%s" % (sys.version_info.major, sys.version_info.minor)

_logger = logging.getLogger(__name__)
try:
    from getmac import get_mac_address as gma
except ImportError:
    _logger.info('\n No se encuentra el módulo -getmac- instalado')
    subprocess.check_call([py_v, "-m", "pip3", "install", "--user", "getmac"])
    from getmac import get_mac_address as gma


class RegistroUsuarios(models.Model):
    _inherit = 'res.users'

    registro_ips = fields.One2many('sicpro.modulo.registro.usuarios_ip', 'users_ip', string='Registros IP')
    registro_macs = fields.One2many('sicpro.modulo.registro.usuarios_mac', 'users_mac', string='Registros MAC')
    validacion_ip_mac = fields.Boolean(default=False, string="Activar Validación IP/MAC")
    direccion_mac = fields.Char(compute='_buscar_mac', string="Dirección MAC")

    def _buscar_mac(self):
        for rec in self:
            rec.direccion_mac = gma()

    def activar_validacion(self):
        for item in self:
            if not item.validacion_ip_mac:
                item.validacion_ip_mac = True

    def desactivar_validacion(self):
        for item in self:
            if item.validacion_ip_mac:
                item.validacion_ip_mac = False


class RegistroMAC(models.Model):
    _name = 'sicpro.modulo.registro.usuarios_mac'
    _description = 'Direcciones MAC de los Usuarios'

    name = fields.Char(string="Descripción")
    mac_address = fields.Char(string="Direcciones MAC")
    users_mac = fields.Many2one('res.users', string='MAC')


class RegistroIP(models.Model):
    _name = 'sicpro.modulo.registro.usuarios_ip'
    _description = 'Direcciones IP de los Usuarios'

    users_ip = fields.Many2one('res.users', string='IP')
    ip_address = fields.Char(string='Direcciones IP')
    nota = fields.Text(string="Notas", required=False)

    # actualizar el comentario de la dirección ip
    @api.onchange('ip_address')
    def _onchange_ip_address(self):
        if self.ip_address == '192.*':
            self.nota = 'El rango de la dirección IP pertenece ' \
                        'a la red local de ETECSA.'
        elif self.ip_address == '172.*':
            self.nota = 'El rango de la dirección IP pertenece ' \
                        'a la red de Teletrabajo.'
        else:
            if self.ip_address:
                self.nota = 'Debe Agregar el comentario referente ' \
                            'al rango IP introducido.'
