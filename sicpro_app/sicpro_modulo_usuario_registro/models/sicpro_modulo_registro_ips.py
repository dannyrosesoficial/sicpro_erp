# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

# Intentar importar la librería de forma segura
try:
    from getmac import get_mac_address as gma
except ImportError:
    gma = None
    _logger.warning(
        'La librería "getmac" no está instalada. Ejecute: pip install getmac')


class RegistroUsuarios(models.Model):
    _inherit = 'res.users'

    registro_ips = fields.One2many('sicpro.modulo.registro.usuarios_ip',
                                   'users_ip', string='Registros IP')
    registro_macs = fields.One2many('sicpro.modulo.registro.usuarios_mac',
                                    'users_mac', string='Registros MAC')
    validacion_ip_mac = fields.Boolean(default=False,
                                       string="Activar Validación IP/MAC")
    direccion_mac = fields.Char(compute='_compute_direccion_mac',
                                string="MAC del Servidor/Cliente Local")

    @api.depends('validacion_ip_mac')
    def _compute_direccion_mac(self):
        for rec in self:
            if gma:
                rec.direccion_mac = gma()
            else:
                rec.direccion_mac = "Librería getmac no disponible"

    def activar_validacion(self):
        self.write({'validacion_ip_mac': True})

    def desactivar_validacion(self):
        self.write({'validacion_ip_mac': False})


class RegistroMAC(models.Model):
    _name = 'sicpro.modulo.registro.usuarios_mac'
    _description = 'Direcciones MAC de los Usuarios'
    _order = 'id desc'

    name = fields.Char(string="Descripción", required=True)
    mac_address = fields.Char(string="Dirección MAC", required=True)
    users_mac = fields.Many2one('res.users', string='Usuario',
                                ondelete='cascade')


class RegistroIP(models.Model):
    _name = 'sicpro.modulo.registro.usuarios_ip'
    _description = 'Direcciones IP de los Usuarios'

    users_ip = fields.Many2one('res.users', string='Usuario',
                               ondelete='cascade')
    ip_address = fields.Char(string='Dirección IP', required=True)
    nota = fields.Text(string="Notas")

    @api.onchange('ip_address')
    def _onchange_ip_address(self):
        if not self.ip_address:
            return

        # Corregido: '192.*' no funciona con == en Python. Usamos startswith.
        if self.ip_address.startswith('192.'):
            self.nota = 'El rango de la dirección IP pertenece a la red local de ETECSA.'
        elif self.ip_address.startswith('172.'):
            self.nota = 'El rango de la dirección IP pertenece a la red de Teletrabajo.'
        else:
            self.nota = 'Debe agregar el comentario referente al rango IP introducido.'
