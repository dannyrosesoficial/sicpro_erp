# -*- coding: utf-8 -*-


from odoo import fields, models, api


class SolicitudesNegociacion(models.Model):
    _inherit = ['sicpro.app.solicitudes.oportunidades']

    herencia_t3 = fields.Char()

    # accion para agregar los seguidores
    def action_pendiente_seguidores(self, ):
        # pendiente para guardar la notificacion en el sistema
        '''self.env['mail.message'].create({
            'message_type': 'notification',
            'body': 'titulo',
            'subtype_id': self.ref('mail.mt_comment').id,
            'subject': 'mensaje subjet',
            'author_id': self.env.user.partner_id.id,
            'model': self._name,
            'res_id': self.id,
            'partner_ids': [(12, 2, self.env.user.partner_id.id)]
        })'''

    # accion del boton de aprovada
    def action_negociacion_aprobar(self, ):
        self.fecha_aprobacion = fields.date.today()
        # creo el id unico de la solicitud
        if not self.id_solicitud:
            # creo el id de la solicitud por proceso y año independiente
            data4 = self.env[
                'sicpro.app.solicitudes.oportunidades'].search_count(
                ['|', ('active', '=', True), ('active', '=', False),
                 ('id_solicitud', '!=', False),
                 ('company_id', '=', self.company_id.id),
                 ('tipo', '=', 'principal'),
                 ('anio', '=', fields.datetime.today().strftime("%Y")), ])
            self.id_solicitud = "SO - " + str(data4 + 1) + "/" + self.anio
            # paso el id de la solicitud a las subsolicitudes
            data2 = self.env['sicpro.app.solicitudes.oportunidades'].search(
                [('solicitud', '=', self.id), ])
            for items in data2:
                items.id_solicitud = self.id_solicitud
        # cambio el estado interno de las solicitudes y subsolicitudes
        self.sudo().estado_interno = 'aprobada'
        data1 = self.env['sicpro.app.solicitudes.oportunidades'].search(
            [('solicitud', '=', self.id), ])
        for items in data1.sudo():
            items.estado_interno = 'aprobada'
            items.fecha_aprobacion = fields.date.today()
            items.message_subscribe(
                partner_ids=self.env['res.users'].sudo().search([
                    ('company_id', '=', items.company_id.id),
                    ('departamento', '=', items.departamento.id),
                    ('groups_id', '=',
                     self.env.ref(
                         'sicpro_app_solicitudes_t4.grupo_app_ejecutor_ejecutor').id)
                ]).partner_id.ids)
            items.message_post(
                body='Iniciativa aprobada.',
                message_type='notification',
                subtype='mail.mt_comment',
                author_id=self.env.user.partner_id.id
            )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t3.solicitudes_negociacion_action').read()[
            0]
        return action

    # accion del boton de restaurar ejecutor
    def action_negociacion_restaurar_ejecutor(self, ):
        # envio la notificacion a los seguidores
        self.message_post(
            body='Iniciativa restaurada.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        self.fecha_aprobacion = fields.date.today()
        self.sudo().tipo = 'subsolicitud'
        self.sudo().estado_interno = 'aprobada'
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t3.solicitudes_negociacion_action').read()[
            0]
        return action


class RechazadasT3(models.TransientModel):
    _name = 'sicpro.app.solicitudes.rechazadas.t3'
    _description = 'Rechazadas T3'

    lost_reason_id = fields.Many2one('sicpro.app.solicitudes.rechazadas',
                                     string="Motivo")

    def action_motivo_rechazo_t3(self):
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Iniciativa rechazada.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # cambio el estado interno de la solicitud
        rechazo = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        for item in rechazo.sudo():
            item.motivo_rechazo = self.lost_reason_id.id
            item.sudo().estado_interno = 'rechazada_dtp'
        # cambio el estado interno de las subsolicitudes
        subsolic = self.env[
            'sicpro.app.solicitudes.oportunidades'].sudo().search(
            [('solicitud', '=', rechazo.id), ])
        for items in subsolic.sudo():
            items.sudo().estado_interno = 'rechazada_dtp'
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t3.solicitudes_negociacion_action').read()[
            0]
        return action


class CanceladasT3(models.TransientModel):
    _name = 'sicpro.app.solicitudes.canceladas.t3'
    _description = 'Canceladas T3'

    motivo_cancelacion = fields.Text(string="Motivo de Cancelación",
                                     required=False, )

    def action_motivo_cancelacion_t3(self):
        # cambio el estado interno de la solicitud
        cancelada = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        for item in cancelada:
            item.motivo_cancelacion = self.motivo_cancelacion
            item.estado_interno = 'cancelada_ejecutor'
        # cambio el estado interno de las subsolicitudes
        for items in self.env['sicpro.app.solicitudes.oportunidades'].search(
                [('solicitud', '=', cancelada.id), ]):
            items.estado_interno = 'cancelada_ejecutor'
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Iniciativa cancelada.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_solicitudes_t3.solicitudes_negociacion_action').read()[
            0]
        return action
