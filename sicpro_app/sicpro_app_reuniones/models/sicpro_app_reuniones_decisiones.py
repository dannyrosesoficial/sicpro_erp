# -*- coding: utf-8 -*-
##############################################################################
#    PROYECTO: SICPRO ERP
#    AUTOR: Daniel Barrero Reyes (Danny Rose's)
#    CONTACTO: daniel.borrero@etecsa.cu
#    Copyright (C) 2020-2026 SICPRO ERP.
#    Todos los derechos reservados.
##############################################################################


from odoo import api, fields, models
from odoo.addons.sicpro_app_administracion.models.constants import \
    MSG_SOPORTE_SICPRO
from odoo.exceptions import ValidationError, UserError


class ReunionesDecisiones(models.Model):
    _name = 'sicpro.app.reuniones.decisiones'
    _description = 'Decisiones de las reuniones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'estado_id asc, fecha_inicio desc'

    # busca él, id específico del modelo de reunion para despachos
    def _busca_etiqueta_despacho(self):
        modelo_reunion = self.env['sicpro.app.reuniones.etiquetas'].search(
            [('despacho', '=', True)]).id
        return modelo_reunion

    name = fields.Char(string='Decisión', default=lambda self: 'Decisión: ',
                       required=True)
    description = fields.Text(string='Descripción', required=True)
    reunion = fields.Many2one('sicpro.app.reuniones.despachos',
                              string="Despacho por Plan", index=True,
                              required=False, tracking=True)
    periodo_reunion = fields.Char(string='Periodo de la reunion',
                                  compute='_periodo_reunion')
    otra_reunion = fields.Char(string='Otro Motivo', required=False,
                               tracking=True)
    company_id = fields.Many2one('res.company', related='reunion.company_id')
    fecha_inicio = fields.Date(string="Fecha inicial", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Fecha Cumplimiento", required=True)
    fecha_pre_fin = fields.Integer(string="fecha_pre_fin")
    responsable_ids = fields.Many2many('res.users',
                                       'decision_responsable_user',
                                       string="Responsable", tracking=True,
                                       readonly=False, required=True, )
    participantes_ids = fields.Many2many('res.users',
                                         'decision_participantes_user',
                                         string="Participantes",
                                         readonly=False, store=True,
                                         domain="[('tipo', '=', 'interno')]")
    cumplimiento = fields.Integer(string='Cumplimiento', store=True)
    estado = fields.Selection(
        [('borrador', 'Borrador'), ('pendiente', 'Pendiente'),
         ('proceso', 'En proceso'), ('revision', 'En Revisión'),
         ('liberar', 'Liberado'), ('cumplido', 'Cumplido'),
         ('cancelado', 'Cancelado')], string='Estados', default='borrador',
        copy=False, tracking=True, group_expand='_group_expand_estados', )
    estado_id = fields.Integer(string='estado_id', default=1)
    consecutivo = fields.Char(string='Consecutivo', tracking=True, copy=False,
                              readonly=True, default=lambda self: 'D-')
    resultado = fields.Html(string='Resultado', required=False, tracking=True)
    cancelado = fields.Text(string='Motivo de cancelación', required=False)
    es_responsable = fields.Boolean(string='Es_responsable',
                                    compute='_compute_es_responsable')
    motivo_rechazo = fields.Text(string='Motivo de Rechazo', tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación",
                                     tracking=True)
    rechazado = fields.Boolean(string='Rechazado', required=False,
                               default=False)
    modelo_reunion = fields.Many2one('sicpro.app.reuniones.etiquetas',
                                     string="Modelo de Reunión",
                                     required=False,
                                     default=_busca_etiqueta_despacho)

    def _group_expand_estados(self, states, domain):
        return [key for key, val in type(self).estado.selection]

    @api.depends('reunion')
    def _periodo_reunion(self):
        if self.reunion:
            fecha = self.reunion.fecha_inicio
            self.periodo_reunion = fecha.date().strftime('%A %d de %B del %Y')
        else:
            self.periodo_reunion = None

    # validar si el usuario es el responsable
    def _compute_es_responsable(self):
        if self.env.user.id in self.responsable_ids.ids:
            self.es_responsable = True
        else:
            self.es_responsable = False

    # pasar a En proceso
    def estado_en_proceso(self):
        if self.participantes_ids:
            self.write(
                {'estado': 'proceso', 'estado_id': 2, 'cumplimiento': 25,
                 'rechazado': False})

            # creo la lista de participantes
            seguidor = self.participantes_ids
            # agrego los participantes al modelo
            self.message_subscribe(partner_ids=seguidor.partner_id.ids)
            # envió la notificación a los seguidores
            self.message_post(body='Decisión asignada',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            for participante in seguidor:
                # envío el correo electrónico
                email_values = {
                    'email_to': participante.partner_id.email_formatted, }
                template = self.env.ref(
                    'sicpro_app_reuniones.reunion_decision_proceso')
                template.send_mail(self.id, force_send=True,
                                   email_values=email_values)
        else:
            raise UserError(
                "Para continuar debe agregar a los ejecutantes de la decisión.")

    # enviar a revision
    def estado_en_revision(self):
        self.write({'estado': 'revision', 'estado_id': 3, 'cumplimiento': 50})

        # envió la notificación a los seguidores
        self.message_post(body='Decisión en revisión',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        for item in self.responsable_ids:
            # envío el correo electrónico al responsable
            email_values = {'email_to': item.email_formatted, }
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_decisión_revision')
            template.send_mail(self.id, force_send=True,
                               email_values=email_values)

    # liberar para revision
    def estado_liberar(self):
        self.write({'estado': 'liberar', 'estado_id': 4, 'cumplimiento': 75})

        # busco usuarios con rol de secretaria y agrego al modelo
        group_secretaria = self.env.ref(
            'sicpro_app_reuniones.group_reuniones_secretaria',
            raise_if_not_found=False)
        secretaria = self.env['res.users']
        if group_validar:
            secretaria = group_secretaria.user_ids
        self.message_subscribe(partner_ids=secretaria.partner_id.ids)

        # no se busca el de director porque ya viene incluido en el rol secretaria
        # group_director = self.env.ref(
        #     'sicpro_app_reuniones.group_reuniones_director',
        #     raise_if_not_found=False)
        # director = self.env['res.users']
        # if group_director:
        #     director = group_director.user_ids
        # self.message_subscribe(partner_ids=director.partner_id.ids)

        # envió la notificación a los seguidores
        self.message_post(body='Decisión liberada',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        # Selecciono el registro de seguidores
        for participante in secretaria:
            # envío el correo electrónico
            email_values = {
                'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_decision_liberar')
            template.send_mail(self.id, force_send=True,
                               email_values=email_values)

    # pasar a cumplido
    def estado_cumplido(self):
        self.write({'estado': 'cumplido', 'estado_id': 5, 'cumplimiento': 100})

        # envió la notificación a los seguidores
        self.message_post(body='Decisión cumplida',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_follower_ids:
            # envío el correo electrónico
            email_values = {
                'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_decision_cumplida')
            template.send_mail(self.id, force_send=True,
                               email_values=email_values)
        # animación de acuerdo cumplido
        rainbow = {'effect': {'fadeout': 'slow',
                              'message': 'Felicidades. La decisión fue cumplida exitosamente',
                              'type': 'rainbow_man', }}
        return rainbow

    # cancelar decisión
    # def estado_cancelado(self):
    #     self.write({'estado': 'cancelado', 'estado_id': 6, 'cumplimiento': 0})
    #     # envió la notificación a los seguidores
    #     self.message_post(body='Decisión cancelada', subtype_xmlid='mail.mt_comment',
    #                       author_id=self.env.user.partner_id.id)
    #     # Selecciono el registro de seguidores
    #     for participante in self.message_follower_ids:
    #         # envío el correo electrónico
    #         email_values = {'email_to': participante.partner_id.email_formatted, }
    #         template = self.env.ref('sicpro_app_reuniones.reunion_decision_cancelada')
    #         template.send_mail(self.id, force_send=True, email_values=email_values)

    # chequea que la fecha fin no sea anterior a la inicial
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_closing_date(self):
        for event in self:
            if event.fecha_fin < event.fecha_inicio:
                raise ValidationError(
                    'La fecha fin no puede ser anterior a la fecha final.' + MSG_SOPORTE_SICPRO)

    @api.model
    def cron_decisiones_vencimiento(self):
        fecha_control = fields.Date.context_today(self)
        data_fechas = self.env['sicpro.app.reuniones.decisiones'].search([(
                                                                          'estado',
                                                                          'in',
                                                                          (
                                                                          'pendiente',
                                                                          'proceso',
                                                                          'revision',
                                                                          'liberar')), ])

        # actualizo los días pre finales
        for item in data_fechas:
            resta = fields.Date.from_string(
                item.fecha_fin) - fields.Date.from_string(fecha_control)
            item.fecha_pre_fin = resta.days

        data = self.env['sicpro.app.reuniones.decisiones'].search(
            [('estado', 'in', ('pendiente', 'proceso', 'revision', 'liberar')),
             ('fecha_pre_fin', '<=', 3)])

        if data:
            for item in data:
                if 3 >= item.fecha_pre_fin > 0:
                    # envió la notificación a los seguidores
                    item.message_post(body='Decisión próxima a vencer',
                                      message_type='notification',
                                      subtype_xmlid='mail.mt_comment',
                                      author_id=self.env.user.partner_id.id)
                    # Selecciono los participantes
                    participantes = item.responsable_ids + item.participantes_ids
                    for participante in participantes:
                        # envío el correo electrónico
                        email_values = {
                            'email_to': participante.email_formatted, }
                        template = self.env.ref(
                            'sicpro_app_reuniones.reunion_decision_proxima_vencer')
                        template.send_mail(item.id, force_send=True,
                                           email_values=email_values)
                elif item.fecha_pre_fin == 0:
                    # envió la notificación a los seguidores
                    item.message_post(body='Decisión vencida',
                                      message_type='notification',
                                      subtype_xmlid='mail.mt_comment',
                                      author_id=self.env.user.partner_id.id)
                    # Selecciono el registro de seguidores
                    for participante in item.message_follower_ids:
                        # envío el correo electrónico
                        email_values = {
                            'email_to': participante.partner_id.email_formatted, }
                        template = self.env.ref(
                            'sicpro_app_reuniones.reunion_decision_vencida')
                        template.send_mail(item.id, force_send=True,
                                           email_values=email_values)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ReunionesDecisiones, self).create(vals_list)
        res.consecutivo = self.env['ir.sequence'].next_by_code(
            'decisiones_consecutivo_incrementar')
        for item in res:
            # creo la lista de seguidores
            responsable = item['responsable_ids']
            # agrego los seguidores al modelo
            item.message_subscribe(partner_ids=responsable.partner_id.ids)
            # envió la notificación a los seguidores
            item.message_post(body='Decisión asignada',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            # envío el correo electrónico
            for val in responsable:
                email_values = {'email_to': val.partner_id.email_formatted}
                template = self.env.ref(
                    'sicpro_app_reuniones.reunion_nueva_decision')
                template.send_mail(item.id, force_send=True,
                                   email_values=email_values, )
                res.write({'estado': 'pendiente'})

        return res


class DecisionesRechazadas(models.TransientModel):
    _name = 'sicpro.app.reuniones.decisiones.rechazadas'
    _description = 'Rechazar decisiones'

    motivo = fields.Text(string="Motivo", required=True)

    def action_motivo_rechazo(self):
        # cambio el estado interno de la solicitud
        rechazo = self.env['sicpro.app.reuniones.decisiones'].browse(
            self.env.context.get('active_ids'))
        for item in rechazo.sudo():
            item.motivo_rechazo = self.motivo
            item.rechazado = True
            item.estado = 'pendiente'
            item.estado_id = 1
            item.cumplimiento = 0  # envió la notificación a los seguidores
        rechazo.message_post(body='Decisión rechazada',
                             subtype_xmlid='mail.mt_comment',
                             author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in rechazo.message_follower_ids:
            # envío el correo electrónico
            email_values = {
                'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_decision_rechazada')
            template.send_mail(rechazo.id, force_send=True,
                               email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_reuniones.action_decisiones_view').sudo().read()[0]
        return action


class DecisionesCanceladas(models.TransientModel):
    _name = 'sicpro.app.reuniones.decisiones.canceladas'
    _description = 'Cancelar decisiones'

    motivo = fields.Text(string="Motivo de Cancelación", required=True, )

    def action_motivo_cancelacion(self):
        # cambio el estado interno de la solicitud
        cancelada = self.env['sicpro.app.reuniones.decisiones'].browse(
            self.env.context.get('active_ids'))
        for item in cancelada:
            item.motivo_cancelacion = self.motivo
            item.estado = 'cancelado'
            item.estado_id = 6
            item.cumplimiento = 0
        # envió la notificación a los seguidores
        cancelada.message_post(body='Decisión cancelada',
                               subtype_xmlid='mail.mt_comment',
                               author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in cancelada.message_follower_ids:
            # envío el correo electrónico
            email_values = {
                'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_decision_cancelada')
            template.send_mail(cancelada.id, force_send=True,
                               email_values=email_values)
        # redirecciono la salida
        action = self.env.ref(
            'sicpro_app_reuniones.action_decisiones_view').sudo().read()[0]
        return action
