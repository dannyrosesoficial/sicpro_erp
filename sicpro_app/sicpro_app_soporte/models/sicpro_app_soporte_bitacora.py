# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SoporteBitacora(models.Model):
    _name = 'sicpro.app.soporte.bitacora'
    _description = 'Bitácora de Usuarios SICPRO'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Selection(string='Actividad',
                            selection=[('crear', 'Crear Usuario'),
                                       ('modificar', 'Modificar Usuario'),
                                       ('eliminar', 'Eliminar Usuario'),
                                       ('vpn_pc', 'VPN PC'),
                                       ('vpn_movil', 'VPN Móvil'), ],
                            required=True, )
    active = fields.Boolean(string="Activo", default=True)
    fecha_solicitud = fields.Date(string='Fecha de Solicitud', required=True,
                                  default=lambda self: fields.Date.context_today(self))
    fecha_ejecucion = fields.Date(string='Fecha de Ejecución', required=True,
                                  default=lambda self: fields.Date.context_today(self))
    ejecutor = fields.Many2one(comodel_name='res.users', string='Ejecutor',
                               required=True,
                               default=lambda self: self.env.uid)
    usuario = fields.Many2one(comodel_name='res.users', string='Usuario',
                              required=True)
    proceso = fields.Many2one(comodel_name='res.company', string='Proceso',
                              related="usuario.company_id", store=True)
    nota = fields.Text(string="Notas", required=False)
    roles = fields.Many2many('sicpro.modulo.roles', string='Roles')

    # Actualiza el comentario se se utiliza la categoría de vpn
    @api.onchange('name')
    def _onchange_name(self):
        if self.name == 'vpn_pc':
            self.nota = 'Este registro es solo de control, la instalación y ' \
                        'configuración del servicio de VPN en la PC corre a ' \
                        'cargo del departamento de TI de la División'
        elif self.name == 'vpn_movil':
            self.nota = 'Se instalo la aplicación Open VPN, se importó ' \
                        'la configuración preestablecida por la empresa y ' \
                        'se activo el servicio de VPN en el móvil del usuario.'
        elif self.name == 'crear':
            self.nota = 'El usuario fue creado correctamente, se le ' \
                        'asignaron los roles y permisos solicitados.'
        elif self.name == 'modificar':
            self.nota = 'El usuario fue modificado correctamente, los roles' \
                        ' y permisos del sistema fueron actualizados'
        elif self.name == 'eliminar':
            self.nota = 'El usuario fue archivado, pasando al estado de' \
                        ' deshabilitado, fueron removidos todos los roles' \
                        ' y permisos que tenia asignado.'
        else:
            self.nota = None
