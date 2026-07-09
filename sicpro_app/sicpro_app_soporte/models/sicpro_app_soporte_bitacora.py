# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SoporteBitacora(models.Model):
    _name = 'sicpro.app.soporte.bitacora'
    _description = 'Bitácora de Usuarios SICPRO'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Selection(string='Actividad',
                            selection=[('crear', 'Crear Usuario'), ('modificar', 'Modificar Usuario'),
                                       ('eliminar', 'Eliminar Usuario'), ('desactivado', 'Desactivación'),
                                       ('reactivado', 'Reactivación'), ('vpn_pc', 'VPN PC'), ('vpn_movil', 'VPN Móvil'),],
                            required=True, )
    active = fields.Boolean(string="Activo", default=True)
    fecha_solicitud = fields.Date(string='Fecha de Solicitud', required=True,
                                  default=lambda self: fields.Date.context_today(self))
    fecha_ejecucion = fields.Date(string='Fecha de Ejecución', required=True,
                                  default=lambda self: fields.Date.context_today(self))
    ejecutor = fields.Many2one(comodel_name='res.users', string='Ejecutor', required=True,
                               default=lambda self: self.env.uid)
    usuario = fields.Many2one(comodel_name='res.users', string='Usuario', required=True)
    proceso = fields.Many2one(comodel_name='res.company', string='Proceso', related="usuario.company_id", store=True)
    nota = fields.Text(string="Notas", required=False)
    roles = fields.Many2many('sicpro.modulo.roles', string='Roles')
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    # Actualiza los roles del usuario
    @api.onchange('usuario')
    def _onchange_usuario(self):
        self.roles = self.usuario.role_line_ids.role_id

    # Actualiza el comentario se se utiliza la categoría de vpn
    @api.onchange('name')
    def _onchange_name(self):
        if self.name == 'vpn_pc':
            self.nota = 'Este registro es solo de control, la instalación y configuración del servicio de VPN ' \
                        'en la PC corre a cargo del departamento de TI de la División'
        elif self.name == 'vpn_movil':
            self.nota = 'Se instaló la aplicación Open VPN, se importó la configuración preestablecida ' \
                        'por la empresa y se activó el servicio de VPN en el móvil del usuario.'
        elif self.name == 'crear':
            self.nota = 'El usuario fue creado correctamente, se le asignaron los roles y permisos solicitados.'
        elif self.name == 'modificar':
            self.nota = 'El usuario fue modificado correctamente, los roles y permisos del sistema fueron actualizados'
        elif self.name == 'eliminar':
            self.nota = 'El usuario fue archivado, pasando al estado de deshabilitado, ' \
                        'fueron removidos todos los roles y permisos que tenía asignado.'
        elif self.name == 'desactivado':
            self.nota = 'El usuario fue archivado, pasando al estado de deshabilitado, ' \
                        'fueron removidos todos los roles y permisos que tenía asignado.'
        elif self.name == 'reactivado':
            self.nota = 'El usuario fue reactivado correctamente, los roles y permisos del sistema fueron actualizados'
        else:
            self.nota = None
