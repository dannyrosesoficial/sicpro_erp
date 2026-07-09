# -*- coding: utf-8

from datetime import date

from odoo import models, fields, api
from odoo.exceptions import UserError


class MediosInformaticosTaller(models.Model):
    _name = 'sicpro.app.medios.informaticos.taller'
    _description = "Medios Informáticos Enviados a Taller"
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.medios.informaticos', 'No. Inventario', )
    no_tique = fields.Char('Tique', required=True)
    active = fields.Boolean('Activo', default=True)
    fecha_entrada = fields.Date('Fecha de Entrada', required=True)
    fecha_recogida = fields.Date('Fecha Recogida', )
    responsable = fields.Char('Responsable en PM', related='name.responsable', store=True, )
    equipo = fields.Char('Equipo', related='name.equipo', store=True, )
    denominacion = fields.Text('Denominación de objeto técnico', related='name.denominacion', store=True, )
    unidad_org = fields.Many2one('sicpro.app.trabajadores.areas', 'Unidad Organizativa', required=True)
    tramite = fields.Many2one('sicpro.app.medios.informaticos.tramites', 'Trámite')
    dictamen_tec = fields.Char('Dictamen Técnico', )
    no_orden_taller = fields.Char('No. Orden Taller')
    tique_cerrado = fields.Boolean('Tique cerrado')
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)

    def notificar_nuevo_registro(self):
        # correo usuario actual
        email_usuario_actual = self.env.user.email_formatted
        # Envío del correo
        email_values = {'email_to': email_usuario_actual, }
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_envio_taller')
        template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

        # Lista de correo de los responsables
        list_responsable = self.env.ref(
            'sicpro_app_medios_informaticos.grupo_app_medios_informaticos_responsable').users
        for responsable in list_responsable:
            # Envío del correo
            email_values = {'email_to': responsable.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_envio_taller')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envió la notificación a los seguidores
            self.message_notify(body='Nuevo envío a taller', subtype_xmlid='mail.mt_comment',
                                author_id=self.env.user.partner_id.id)

        if self.responsable:
            # correo usuario responsable del equipo
            email_responsable_equipo = self.name.trabajador_id.correo_trabajo
            # envío del correo
            email_values = {'email_to': email_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_envio_taller')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

            # correo jefe usuario responsable del equipo
            email_jefe_responsable_equipo = self.name.trabajador_id.parent_id.correo_trabajo
            # envío del correo
            email_values = {'email_to': email_jefe_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_envio_taller')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    @api.model
    def create(self, vals):
        res = super(MediosInformaticosTaller, self).create(vals)

        '''medios_informaticos_taller = self.env['sicpro.app.medios.informaticos.taller'].search([
            '&', ('name', '=', res['name'].name), ('tique_cerrado', '=', False), ('id', '!=', res['id'])])
        if medios_informaticos_taller:
            raise UserError('Este medio se encuentra en taller con el tique aún abierto,'
                        ' verifíquelo. Si cree que es un error contacte al administrador')'''

        medio_informatico = self.env['sicpro.app.medios.informaticos'].search([('name', '=', res['name'].name)])
        if medio_informatico:
            medio_informatico.sudo().write({'estado': 'taller'})

        res.notificar_nuevo_registro()

        return res

    def cerrar_tique(self):
        self.name.estado = 'funcionando'
        self.tique_cerrado = True

        # correo usuario actual
        email_usuario_actual = self.env.user.email_formatted
        # Envío del correo
        email_values = {'email_to': email_usuario_actual, }
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_cerrar_tique')
        template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

        # Lista de correo de los responsables
        list_responsable = self.env.ref(
            'sicpro_app_medios_informaticos.grupo_app_medios_informaticos_responsable').users
        for responsable in list_responsable:
            # Envío del correo
            email_values = {'email_to': responsable.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_cerrar_tique')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envió la notificación a los seguidores
            self.message_post(body='Nuevo envío a taller', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

        if self.responsable:
            # correo usuario responsable del equipo
            email_responsable_equipo = self.name.trabajador_id.correo_trabajo
            # envío del correo
            email_values = {'email_to': email_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_cerrar_tique')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

            # correo jefe usuario responsable del equipo
            email_jefe_responsable_equipo = self.name.trabajador_id.parent_id.correo_trabajo
            # envío del correo
            email_values = {'email_to': email_jefe_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_cerrar_tique')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    @api.constrains('fecha_recogida')
    def restriccion_fecha_recogida(self):
        if self.fecha_recogida:
            if self.fecha_recogida < self.fecha_entrada:
                raise UserError('La fecha de recogida no puede ser menor que la fecha de entrada,'
                                ' verifíquelo. Si cree que es un error contacte al administrador')

    @api.constrains('fecha_entrada')
    def restriccion_fecha_entrada(self):
        if self.fecha_entrada:
            today = date.today()
            if self.fecha_entrada > today:
                raise UserError('La fecha de entrada no puede ser mayor al día de hoy,'
                                ' verifíquelo. Si cree que es un error contacte al administrador')
