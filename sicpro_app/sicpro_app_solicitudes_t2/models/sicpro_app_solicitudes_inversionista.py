# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class SolicitudesInversionista(models.Model):
    _inherit = ['sicpro.app.solicitudes.oportunidades']

    herencia_t2 = fields.Char()

    # accion del boton de liberar
    def action_inversionista_liberar(self, ):
        # Agrego seguidores de negocios
        usuario = self.env['res.users'].sudo().search(
            [('company_id', '=', self.company_id.id),
             ('groups_id', '=', self.env.ref(
                 'sicpro_app_solicitudes_t3.grupo_app_negocio_ejecutor').id)
             ])
        self.message_subscribe(partner_ids=usuario.partner_id.ids)

        # Agrego seguidores de negocios de las subsolicitudes
        iniciativas = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])
        for items in iniciativas.sudo():
            items.message_subscribe(partner_ids=self.env['res.users'].sudo().search(
                [('company_id', '=', self.company_id.id),
                 ('groups_id', '=', self.env.ref(
                     'sicpro_app_solicitudes_t3.grupo_app_negocio_ejecutor').id)
                 ]).partner_id.ids)

        # envio notificacion a los seguidores de negocios
        self.message_post(
            body='Iniciativa creada para negocio.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )

        # cambio el estado interno de las solicitudes y subsolicitudes
        self.sudo().estado_interno = 'liberada'
        # cambio el estado interno de las subsolicitudes
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])
        for items in iniciativa.sudo():
            items.estado_interno = 'liberada'
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t2.solicitudes_inversionista_action').read()[0]
        return action

    # accion del boton de restaurar solicitud rechazada
    def action_inversionista_restaurar_rechazada(self, ):
        # envio notificacion a los seguidores de negocios
        self.message_post(
            body='Iniciativa restaurada para negocio.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # cambio el estado interno de las solicitudes y subsolicitudes
        self.sudo().estado_interno = 'liberada'
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])
        for items in iniciativa.sudo():
            items.estado_interno = 'liberada'
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t2.solicitudes_inversionista_action').read()[0]
        return action

    # accion del boton de cancelar
    def action_inversionista_cancelar(self, ):
        self.estado_interno = 'cancelada_cliente'
        # cambio el estado interno de las subsolicitudes
        for items in self.env['sicpro.app.solicitudes.oportunidades'].search(
                [('solicitud', '=', self.id), ]):
            items.estado_interno = self.estado_interno
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t2.solicitudes_inversionista_action').read()[0]
        return action

    # accion del boton de restaurar solicitud cancelada
    def action_inversionista_restaurar_cancelada(self, ):
        self.sudo().estado_interno = 'liberada'
        # cambio el estado interno de las subsolicitudes
        iniciativa = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])
        for items in iniciativa.sudo():
            items.estado_interno = 'liberada'
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t2.solicitudes_inversionista_action').read()[0]
        return action


class CanceladasT2(models.TransientModel):
    _name = 'sicpro.app.solicitudes.canceladas.t2'
    _description = 'Canceladas T2'

    motivo_cancelacion = fields.Text(string="Motivo de Cancelación",
                                     required=False, )

    def action_motivo_cancelacion_t2(self):
        # cambio el estado interno de la solicitud
        cancelada = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        for item in cancelada:
            item.motivo_cancelacion = self.motivo_cancelacion
            item.estado_interno = 'cancelada_cliente'
        # cambio el estado interno de las subsolicitudes
        for items in self.env['sicpro.app.solicitudes.oportunidades'].search(
                [('solicitud', '=', cancelada.id), ]):
            items.estado_interno = 'cancelada_cliente'
        action = self.env.ref(
            'sicpro_app_solicitudes_t2.solicitudes_inversionista_action').read()[0]
        return action
