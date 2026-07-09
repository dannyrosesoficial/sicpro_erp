# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class MediosInformaticosBajas(models.Model):
    _name = 'sicpro.app.medios.informaticos.bajas'
    _description = "Baja de Medios Informáticos"
    _inherit = ['mail.thread']

    name = fields.Many2one('sicpro.app.medios.informaticos.taller', 'No. de Inventario', required=True,
                           domain="[('tique_cerrado', '=', False)]", )
    active = fields.Boolean('Activo', default=True)
    denominacion = fields.Text('Denominación del Equipo', related='name.denominacion', store=True, )
    no_orden_mtto_taller = fields.Char('No. de Orden de Mantenimiento Taller', required=True, )
    dictamen_tec = fields.Char('Dictamen Técnico de SERTOD No. de Orden de Trabajo', required=True, )
    unidad_org = fields.Many2one('sicpro.app.trabajadores.areas', 'Unidad Organizativa', related='name.unidad_org',
                                 store=True, )
    fecha_ent_exp_economia = fields.Date('Fecha de Entrega del Expediente a Economía', )
    no_acta_acuerdo_consejo_dir = fields.Char('No. de Acta y Acuerdo del Consejo de Dirección', )
    fecha_acta_destino_final = fields.Date('Fecha del Acta de Destino Final', )
    acta_entrega_sertod = fields.Char('Acta de Entrega a SERTOD', )
    no_exp_economia = fields.Char('No. de Expediente de Economía', )
    company_id = fields.Many2one('res.company', string='Proceso', required=True, default=lambda self: self.env.company)

    def notificar_nuevo_registro(self):
        # correo usuario actual
        email_usuario_actual = self.env.user.email_formatted
        # Envío del correo
        email_values = {'email_to': email_usuario_actual, }
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_baja')
        template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

        # Lista de correo de los responsables
        list_responsable = self.env.ref(
            'sicpro_app_medios_informaticos.grupo_app_medios_informaticos_responsable').users
        for responsable in list_responsable:
            # Envío del correo
            email_values = {'email_to': responsable.email_formatted, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_baja')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)
            # envió la notificación a los seguidores
            self.message_notify(body='Baja de medio informático', subtype_xmlid='mail.mt_comment',
                                author_id=self.env.user.partner_id.id)

        if self.name.responsable:
            # correo usuario responsable del equipo
            email_responsable_equipo = self.name.name.trabajador_id.correo_trabajo
            # envio del correo
            email_values = {'email_to': email_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_baja')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

            # correo jefe usuario responsable del equipo
            email_jefe_responsable_equipo = self.name.name.trabajador_id.parent_id.correo_trabajo
            # envío del correo
            email_values = {'email_to': email_jefe_responsable_equipo, }
            local_context = self.env.context.copy()
            template = self.env.ref('sicpro_app_medios_informaticos.medios_informaticos_baja')
            template.with_context(local_context).send_mail(self.id, force_send=True, email_values=email_values)

    @api.model
    def create(self, vals_list):
        res = super(MediosInformaticosBajas, self).create(vals_list)

        medio_informatico = self.env['sicpro.app.medios.informaticos'].search([('name', '=', res['name'].name.name)])
        medio_informatico_taller = self.env['sicpro.app.medios.informaticos.taller'].search(
            [('name', '=', res['name'].name.name)])
        if medio_informatico:
            medio_informatico.sudo().write({'archivado': True, 'active': False, 'estado': 'baja'})

        if medio_informatico_taller:
            medio_informatico_taller.sudo().write({'active': False})

        res.notificar_nuevo_registro()

        return res
