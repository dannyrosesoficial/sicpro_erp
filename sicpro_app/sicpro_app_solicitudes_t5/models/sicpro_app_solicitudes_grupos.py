# -*- coding: utf-8 -*-


from odoo import fields, models, api


class SolicitudesGrupos(models.Model):
    _inherit = ['sicpro.app.solicitudes.oportunidades']

    herencia_t5 = fields.Char()
    oportunidad_id = fields.Many2one(
        comodel_name="sicpro.app.solicitudes.oportunidades")


class RechazadasT5(models.TransientModel):
    _name = 'sicpro.app.solicitudes.rechazadas.t5'
    _description = 'Rechazadas T5'

    lost_reason_id = fields.Many2one('sicpro.app.solicitudes.rechazadas',
                                     string="Motivo")

    def action_motivo_rechazo_t5(self):
        # cambio el estado interno de la subsolicitud
        rechazo = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        for item in rechazo:
            item.motivo_rechazo = self.lost_reason_id.id
            item.estado_interno = 'rechazada_agrupacion'
            item.type = 'iniciativa'
            item.tipo = 'subsolicitud'
        # llamo al metodo para crear la notificacion
        post = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        post.message_post(
            body='Oportunidad rechazada.',
            message_type='notification',
            subtype='mail.mt_comment',
            author_id=self.env.user.partner_id.id
        )
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes_t5.solicitudes_grupos_action').read()[0]
        return action


class GrupoEjecutorT5(models.TransientModel):
    _name = 'sicpro.app.grupo.ejecutor.t5'
    _description = 'Grupo Ejecutor T5'

    departament_id = fields.Integer(
        default=lambda self: self.env['sicpro.app.solicitudes.oportunidades'].browse(
        self.env.context.get('active_ids')).departamento.id)
    grupo_id = fields.Integer()
    team_id = fields.Many2one('sicpro.app.solicitudes.grupo.ejecutor',
                              string='Grupo Ejecutor',
                              tracking=True, required=True)
    jefe_grupo = fields.Many2one(comodel_name="sicpro.app.trabajadores.general",
                                 string='Líder del grupo',
                                 related="team_id.jefe_grupo", required=False)
    especialista_ejecutor = fields.Many2one(
        comodel_name="sicpro.app.trabajadores.general", string='Asignar a', )

    # accion para trae el id del grupo
    @api.onchange('team_id')
    def _onchange_team_id(self, ):
        self.grupo_id = self.team_id.id

    def action_grupo_ejecutor_t5(self, ):
        # cambio el estado interno de la subsolicitud
        oportunidad = self.env['sicpro.app.solicitudes.oportunidades'].browse(
            self.env.context.get('active_ids'))
        for item in oportunidad.sudo():
            item.team_id = self.team_id
            item.jefe_grupo = self.jefe_grupo
            item.especialista_ejecutor = self.especialista_ejecutor
            if self.especialista_ejecutor:
                item.stage_id = 2
            else:
                item.stage_id = 1
            # Agrego seguidores para grupo ejecutor
            if item.jefe_grupo:
                item.message_subscribe(
                    partner_ids=item.jefe_grupo.user_id.partner_id.ids)
            if item.especialista_ejecutor:
                item.message_subscribe(
                    partner_ids=item.especialista_ejecutor.user_id.partner_id.ids)
            # envio notificacion a los seguidores de negocios
            item.message_post(
                body='oportunidad transferida.',
                message_type='notification',
                subtype='mail.mt_comment',
                author_id=self.env.user.partner_id.id
            )
        # redirecciono la salida
        action = self.env.ref('sicpro_app_solicitudes_t5.solicitudes_grupos_action').read()[0]
        return action
