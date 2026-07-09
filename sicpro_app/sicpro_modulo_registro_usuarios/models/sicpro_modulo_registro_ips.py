
from odoo import models, fields


class RegistroUsuarios(models.Model):
    _inherit = 'res.users'

    registro_ips = fields.One2many('sicpro.modulo.registro.usuarios_ip',
                                   'users_ip', string='IP')


class RegistroIP(models.Model):
    _name = 'sicpro.modulo.registro.usuarios_ip'
    _description = 'Direcciones IP de los Usuarios'

    users_ip = fields.Many2one('res.users', string='IP')
    ip_address = fields.Char(string='Direcciones IP')
    nota = fields.Text(string="Notas", required=False)
