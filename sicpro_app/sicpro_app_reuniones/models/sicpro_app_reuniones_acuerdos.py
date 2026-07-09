# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ReunionesAcuerdos(models.Model):
    _name = 'sicpro.app.reuniones.acuerdos'
    _description = 'Acuerdos de las reuniones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'estado_id asc, fecha_inicio desc'

    @api.model
    def default_get(self, vals):
        res = super(ReunionesAcuerdos, self).default_get(vals)
        if 'name' in vals and (not res.get('name') or res['name'] == _('Titulo')) and self.env.context.get(
                'default_event_name'):
            res['name'] = _('Acuerdo para %s', self.env.context['default_event_name'] + '......')
        return res

    def _check_readonly_admin(self):
        import odoo.addons.nucleo_sicpro_erp.models.sicpro_app_nucleo as nucleo_readonly_check
        for item in self:
            item.readonly_admin = nucleo_readonly_check.NucleoReadonly.nucleo_readonly_check(self)

    name = fields.Char(string='Acuerdo', default=lambda self: _('Titulo'), required=True)
    description = fields.Text('Description',  tracking=True)
    reunion = fields.Many2one('sicpro.app.reuniones', string="Reunión", index=True, )
    company_id = fields.Many2one('res.company', related='reunion.company_id')
    fecha_inicio = fields.Date(string="Fecha inicial", required=True, default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Fecha Cumplimiento", required=True)
    fecha_pre_fin = fields.Integer(string="fecha_pre_fin")
    responsable_ids = fields.Many2many('res.users', 'acuerdos_responsable_user', string="Responsable", tracking=True,
                                       readonly=False, required=True,)
    participantes_ids = fields.Many2many('res.users', 'acuerdos_participantes_user', string="Participantes",
                                         readonly=False, store=True,  tracking=True, domain="[('tipo', '=', 'interno')]")
    cumplimiento = fields.Integer(string='Cumplimiento', store=True)
    estado = fields.Selection(
        [('pendiente', 'Pendiente'), ('proceso', 'En proceso'), ('revision', 'En Revisión'), ('liberar', 'Liberado'),
         ('cumplido', 'Cumplido'), ('cancelado', 'Cancelado')], string='Estados', default='pendiente',
        copy=False, tracking=True, group_expand='_group_expand_estados',)
    estado_id = fields.Integer('estado_id', default=1)
    negociar_terminos = fields.Boolean(string='Negociar Términos', required=False)
    tipo_reunion = fields.Selection(string='Tipo Reunión',
                                    selection=[('presencial', 'Presencial'), ('distancia', 'A Distancia'), ],
                                    default='presencial', required=True, )
    modo_distancia = fields.Selection(string='Modo Distancia',
                                      selection=[('correo', 'Correo electrónico'), ('audio', 'AudioConferencia'),
                                          ('video', 'VideoConferencia'), ], required=False, )
    modelo_reunion = fields.Many2one('sicpro.app.reuniones.etiquetas', related='reunion.modelo_reunion',
                                     string="Modelo de Reunión", store=True)
    resultado = fields.Html(string='Resultado', required=False, tracking=True)
    cancelado = fields.Text(string='Motivo de cancelación', required=False)
    es_responsable = fields.Boolean(string='Es_responsable', compute='_compute_es_responsable')
    motivo_rechazo = fields.Text(string='Motivo de Rechazo', tracking=True)
    motivo_cancelacion = fields.Text(string="Motivo de Cancelación", tracking=True)
    rechazado = fields.Boolean(string='Rechazado', required=False, default=False)
    readonly_admin = fields.Boolean(compute='_check_readonly_admin')

    def _group_expand_estados(self, states, domain, order):
        return [key for key, val in type(self).estado.selection]

    # validar si el usuario es el responsable
    def _compute_es_responsable(self):
        if self.env.user.id in self.responsable_ids.ids:
            self.es_responsable = True
        else:
            self.es_responsable = False

    # pasar a En proceso
    def estado_en_proceso(self):
        if self.participantes_ids:
            self.write({'estado': 'proceso', 'estado_id': 2, 'cumplimiento': 25, 'rechazado': False})

            # creo la lista de participantes
            seguidor = self.participantes_ids
            # agrego los seguidores al modelo
            self.message_subscribe(partner_ids=seguidor.partner_id.ids)
            # envió la notificación a los seguidores
            self.message_post(body='Acuerdo asignado', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            for participante in seguidor:
                # envío el correo electrónico
                email_values = {'email_to': participante.partner_id.email_formatted, }
                template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_proceso')
                template.send_mail(self.id, force_send=True, email_values=email_values)
        else:
            raise UserError("Para continuar debe agregar a los ejecutantes del acuerdo.")

    # enviar a revision
    def estado_en_revision(self):
        self.write({'estado': 'revision', 'estado_id': 3, 'cumplimiento': 50})
        # envió la notificación a los seguidores
        self.message_post(body='Acuerdo en revisión', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        for item in self.responsable_ids:
            # envío el correo electrónico al responsable
            email_values = {'email_to': item.email_formatted, }
            template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_revision')
            template.send_mail(self.id, force_send=True, email_values=email_values)

    # liberar para revision
    def estado_liberar(self):
        self.write({'estado': 'liberar', 'estado_id': 4, 'cumplimiento': 75})

        # busco usuarios con rol de secretaria y agrego al modelo
        secretaria = self.env.ref('sicpro_app_reuniones.group_reuniones_secretaria').users
        self.message_subscribe(partner_ids=secretaria.partner_id.ids)

        # no se busca el de director porque ya viene incluido en el rol secretaria
        # director = self.env.ref('sicpro_app_reuniones.group_reuniones_director').users
        # self.message_subscribe(partner_ids=director.partner_id.ids)

        # envió la notificación a los seguidores
        self.message_post(body='Acuerdo liberado', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)

        # Selecciono el registro de seguidores
        for participante in secretaria:
            # envío el correo electrónico
            email_values = {'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_liberar')
            template.send_mail(self.id, force_send=True, email_values=email_values)

    # pasar a cumplido
    def estado_cumplido(self):
        self.write({'estado': 'cumplido', 'estado_id': 5, 'cumplimiento': 100})

        # envió la notificación a los seguidores
        self.message_post(body='Acuerdo cumplido', subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in self.message_follower_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_cumplido')
            template.send_mail(self.id, force_send=True, email_values=email_values)
        rainbow = {
            'effect': {'fadeout': 'slow', 'message': 'Felicidades. El Acuerdo fue cumplido exitosamente',
                       'type': 'rainbow_man', }}
        return rainbow

    # chequea que la fecha fin no sea anterior a la inicial
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_closing_date(self):
        for event in self:
            if event.fecha_fin < event.fecha_inicio:
                raise ValidationError(_('La fecha fin no puede ser anterior a la fecha final.'))

    @api.model
    def acuerdos_vencimiento(self):
        fecha_control = fields.Date.context_today(self)
        data_fechas = self.env['sicpro.app.reuniones.acuerdos'].search(
            [('estado', 'in', ('pendiente', 'proceso', 'revision', 'liberar')), ])

        # actualizo los días pre finales
        for item in data_fechas:
            resta = fields.Date.from_string(item.fecha_fin) - fields.Date.from_string(fecha_control)
            item.fecha_pre_fin = resta.days

        data = self.env['sicpro.app.reuniones.acuerdos'].search(
            [('estado', 'in', ('pendiente', 'proceso', 'revision', 'liberar')), ('fecha_pre_fin', '<=', 3)])

        if data:
            for item in data:
                if 3 >= item.fecha_pre_fin > 0:
                    # envió la notificación a los seguidores
                    item.message_post(body='Acuerdo próximo a vencer', message_type='notification',
                                      subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
                    # Selecciono los participantes
                    participantes = item.responsable_ids + item.participantes_ids
                    for participante in participantes:
                        # envío el correo electrónico
                        email_values = {'email_to': participante.partner_id.email_formatted, }
                        template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_proximo_vencer')
                        template.send_mail(item.id, force_send=True, email_values=email_values)
                elif item.fecha_pre_fin == 0:
                    # envió la notificación a los seguidores
                    item.message_post(body='Acuerdo vencido', message_type='notification',
                                      subtype_xmlid='mail.mt_comment', author_id=self.env.user.partner_id.id)
                    # Selecciono el registro de seguidores
                    for participante in item.message_follower_ids:
                        # envío el correo electrónico
                        email_values = {'email_to': participante.partner_id.email_formatted, }
                        template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_vencido')
                        template.send_mail(item.id, force_send=True, email_values=email_values)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ReunionesAcuerdos, self).create(vals_list)
        for item in res:
            # creo la lista de seguidores
            responsable = item['responsable_ids']
            # agrego los seguidores al modelo
            item.message_subscribe(partner_ids=responsable.partner_id.ids)
            # envió la notificación a los seguidores
            item.message_post(body='Acuerdo asignado', subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            # envío el correo electrónico
            for val in responsable:
                email_values = {'email_to': val.email_formatted}
                template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo')
                template.send_mail(item.id, force_send=True, email_values=email_values,)

        return res


class AcuerdosRechazados(models.TransientModel):
    _name = 'sicpro.app.reuniones.acuerdos.rechazados'
    _description = 'Rechazar decisiones'

    motivo = fields.Text(string="Motivo", required=True)

    def action_motivo_rechazo(self):
        # cambio el estado interno de la solicitud
        rechazo = self.env['sicpro.app.reuniones.acuerdos'].browse(self.env.context.get('active_ids'))
        for item in rechazo.sudo():
            item.motivo_rechazo = self.motivo
            item.rechazado = True
            item.estado = 'pendiente'
            item.estado_id = 1
            item.cumplimiento = 0  # envió la notificación a los seguidores
        rechazo.message_post(body='Acuerdo rechazado', subtype_xmlid='mail.mt_comment',
                             author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in rechazo.message_follower_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_rechazado')
            template.send_mail(rechazo.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_reuniones.action_acuerdos_view').sudo().read()[0]
        return action


class AcuerdosCancelados(models.TransientModel):
    _name = 'sicpro.app.reuniones.acuerdos.cancelados'
    _description = 'Cancelar decisiones'

    motivo = fields.Text(string="Motivo de Cancelación", required=True, )

    def action_motivo_cancelacion(self):
        # cambio el estado interno de la solicitud
        cancelada = self.env['sicpro.app.reuniones.acuerdos'].browse(self.env.context.get('active_ids'))
        for item in cancelada:
            item.motivo_cancelacion = self.motivo
            item.estado = 'cancelado'
            item.estado_id = 6
            item.cumplimiento = 0
        # envió la notificación a los seguidores
        cancelada.message_post(body='Acuerdo cancelado', subtype_xmlid='mail.mt_comment',
                               author_id=self.env.user.partner_id.id)
        # Selecciono el registro de seguidores
        for participante in cancelada.message_follower_ids:
            # envío el correo electrónico
            email_values = {'email_to': participante.partner_id.email_formatted, }
            template = self.env.ref('sicpro_app_reuniones.reunion_nuevo_acuerdo_cancelado')
            template.send_mail(cancelada.id, force_send=True, email_values=email_values)
        # redirecciono la salida
        action = self.env.ref('sicpro_app_reuniones.action_acuerdos_view').sudo().read()[0]
        return action