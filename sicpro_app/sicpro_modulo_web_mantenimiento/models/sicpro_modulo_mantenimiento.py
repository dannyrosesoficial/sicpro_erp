# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SicproMantenimiento(models.Model):
    _name = 'sicpro.modulo.web.mantenimiento'
    _description = 'Módulo para la puesta en mantenimiento de SICPRO ERP'

    name = fields.Char(string='Acción', default='MODO MANTENIMIENTO')
    activar_mantenimiento = fields.Boolean(string='Activar Mantenimiento', required=False)
    fecha_activacion = fields.Datetime(string='Fecha Activación', required=True)
    servidor_ldap = fields.Many2one(comodel_name='res.company.ldap', string='Servidor LDAP',
                                    domain="['|', ('active', '=', True), ('active', '=', False)]", required=True)
    servidor_correo_saliente = fields.Many2one(comodel_name='ir.mail_server', string='Servidor Correo Saliente',
                                               domain="['|', ('active', '=', True), ('active', '=', False)]",
                                               required=True)
    servidor_correo_entrante = fields.Many2one(comodel_name='fetchmail.server', string='Servidor Correo Entrante',
                                               domain="['|', ('active', '=', True), ('active', '=', False)]",
                                               required=True)
    active = fields.Boolean(string='Archivado', default=True)

    @api.constrains('active')
    def _check_id_unico(self):
        uniq = self.env['sicpro.modulo.web.mantenimiento'].search(['&', ("active", "=", True), ("id", "!=", self.id)])
        if uniq:
            raise ValidationError(_("¡Ya se encuentra un modo de mantenimiento configurado!. "
                                    "Si cree que es un error contacte al administrador"))

    # verífico la fecha de reactivación
    @api.constrains('fecha_activacion')
    def _check_fecha_activacion(self):
        hoy = fields.Datetime.now()
        if self.fecha_activacion and hoy >= self.fecha_activacion:
            raise ValidationError(_("¡La fecha de reactivación no puede ser menor a la fecha actual!. "
                                    "Si cree que es un error contacte al administrador"))

    # activo o desactivo el modo de mantenimiento
    @api.onchange('activar_mantenimiento')
    def onchange_activar_mantenimiento(self):
        # busco los registros desactivadores de usuarios
        desactivar = self.env['sicpro.app.modulo.usuario.desactivar'].search([])
        backup = self.env['ir.cron'].sudo().search(
            ['|', ('active', '=', True), ('active', '=', False),
             ('id', '=', self.env.ref('sicpro_modulo_backup_server.ir_cron_auto_db_backup').id)])

        hoy = fields.Datetime.now()
        if self.fecha_activacion and hoy >= self.fecha_activacion:
            raise ValidationError(_("¡La fecha de reactivación no puede ser menor a la fecha actual!. "
                                    "Si cree que es un error contacte al administrador"))
        else:
            if self.activar_mantenimiento:
                # desactivo el servidor de ldap
                self.servidor_ldap.active = False
                # desactivo el servidor de correos Saliente
                self.servidor_correo_saliente.active = False
                # desactivo el servidor de correos entrantes
                self.servidor_correo_entrante.active = False
                # desactivar los desactivadores de usuarios
                for item in desactivar:
                    item.name = False
                # desactivo el cron de ejecución de los backups y sincronización automatizada
                backup.active = False
            else:
                # activo el servidor de ldap
                self.servidor_ldap.active = True
                # activo el servidor de correos Saliente
                self.servidor_correo_saliente.active = True
                # activo el servidor de correos entrantes
                self.servidor_correo_entrante.active = True
                # activo los desactivadores de usuarios
                for item in desactivar:
                    item.name = True
                # activo el cron de ejecución de los backups y sincronización automatizada
                backup.active = True
