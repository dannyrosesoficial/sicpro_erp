# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MassMailingContact(models.Model):
    _inherit = 'mailing.contact'

    usuario = fields.Many2one('res.users', string='Buscar Usuarios', required=False,
                              domain="[('marketing_contacto', '=', False)]", )
    usuario_temp = fields.Many2one('res.users', string='Usuarios Temporal', required=False, )
    usuario_sistema = fields.Boolean(string='Usuario del Sistema', required=False, default=False)
    ocupacion_id = fields.Many2one('sicpro.app.trabajadores.ocupacion', 'Puesto de Trabajo', required=False,
                                   related="usuario.ocupacion_id")
    active = fields.Boolean(string='Archivar', required=False, default=True)
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)

    @api.constrains('usuario')
    def _check_usuario_unico(self):
        self.ensure_one()
        uniq = self.env['mailing.contact'].search(['&', ("usuario", "=", self.usuario.name), ("id", "!=", self.id)])
        if self.usuario:
            # Verífico la duplicidad del usuario
            if uniq:
                raise ValidationError(_("¡El usuario introducido ya existe!. "
                                        "Si cree que es un error contacte al administrador"))
            else:
                # ejecuto la vinculación del contacto con el usuario
                marketing = self._origin.id
                user_temp = self.usuario_temp.id
                self.env['res.users'].search([('id', '=', user_temp)]).write({'marketing_contacto': None})

                user = self.usuario.id
                self.env['res.users'].search([('id', '=', user)]).write({'marketing_contacto': marketing})
                self.usuario_temp = self.usuario

    @api.onchange('usuario')
    def onchange_usuario(self):
        if self.usuario:
            self.usuario_sistema = True
            self.email = self.usuario.email
            self.name = self.usuario.name
            self.company_name = self.usuario.company_id.identificador_corto
            self.country_id = self.usuario.company_id.country_id
        else:
            self.usuario_sistema = False
            self.email = None
            self.name = None
            self.company_name = None
            self.country_id = None
            user_temp = self.usuario_temp.id
            self.env['res.users'].search([('id', '=', user_temp)]).write({'marketing_contacto': None})
            self.usuario_temp = None

    # sincroniza el estado de los usuarios, agrega o archiva en dependencia del estado
    def marketing_usuario_cron(self):
        usuarios_sistema = self.env['res.users'].search(['|', ('active', '=', True), ('active', '=', False)])

        for item in usuarios_sistema:
            usuarios_marketing = self.env['mailing.contact'].search(
                ['|', '&', ('active', '=', True), ('active', '=', False), ('id', '=', item.marketing_contacto.id)])

            # compruebo que exista el usuario
            if usuarios_marketing:
                # existe y lo actualizo con el estado del sistema
                usuarios_marketing.active = item.active
            else:
                # verífico que el usuario que voy a crear esta activo
                if item.active:
                    # no existe, procedo a agregarlo
                    value = {'usuario': item.id, 'usuario_sistema': True, 'email': item.email, 'name': item.name,
                             'company_name': item.company_id.identificador_corto,
                             'country_id': item.company_id.country_id.id}

                    # creo el registro con el nuevo contacto
                    contacto = self.env['mailing.contact'].create(value)
                    # actualizo la vinculación del contacto del marketing con el usuario
                    item.marketing_contacto = contacto

                    # envío el correo de aviso de nuevo contacto creado
                    # busco los usuarios con permisos a recibir los correos de alerta
                    usuarios = self.env['res.users'].sudo().search([('groups_id', 'in', self.env.ref(
                        'sicpro_app_administracion.grupo_app_administracion_admin').id)])

                    for value in usuarios:
                        # envío el correo electrónico
                        email_values = {'email_to': value.email_formatted, }
                        template = self.env.ref('sicpro_app_marketing.marketing_usuario_contacto')
                        template.send_mail(contacto.id, force_send=True, email_values=email_values)