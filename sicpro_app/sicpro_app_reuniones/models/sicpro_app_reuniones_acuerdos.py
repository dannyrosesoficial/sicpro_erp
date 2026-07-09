# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import pytz

from odoo.fields import Date


class ReunionesAcuerdos(models.Model):
    _name = 'sicpro.app.reuniones.acuerdos'
    _description = 'Acuerdos de las reuniones'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'estado_id asc, fecha_inicio desc'

    @api.model
    def default_get(self, fields):
        res = super(ReunionesAcuerdos, self).default_get(fields)
        if 'name' in fields and (not res.get('name') or res['name'] == _(
                'Titulo')) and self.env.context.get('default_event_name'):
            res['name'] = _('Acuerdo para %s',
                            self.env.context['default_event_name'] + '......')
        return res

    name = fields.Char(string='Acuerdo', default=lambda self: _('Titulo'),
                       required=True)
    description = fields.Text('Description', )
    reunion = fields.Many2one('sicpro.app.reuniones', string="Reunión",
                              index=True, )
    company_id = fields.Many2one('res.company', related='reunion.company_id')
    fecha_inicio = fields.Date(string="Fecha inicial", required=True,
                               default=lambda self: fields.Datetime.now())
    fecha_fin = fields.Date(string="Fecha Cumplimiento", required=True)
    fecha_pre_fin = fields.Integer(string="fecha_pre_fin")
    responsable_id = fields.Many2one('res.users', string='Responsable',
                                     tracking=True, required=True, )
    cargo_responsable = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                        string='Cargo', tracking=True,
                                        related='responsable_id.ocupacion_id')
    participantes_ids = fields.Many2many('res.users', string="Participantes",
                                         readonly=False, store=True,
                                         domain="[('tipo', '=', 'interno')]")
    cumplimiento = fields.Integer(string='Cumplimiento', store=True)
    estado = fields.Selection(
        [('pendiente', 'Pendiente'), ('proceso', 'En proceso'),
         ('revision', 'En Revisión'), ('liberar', 'Liberar'),
         ('cumplido', 'Cumplido'), ('cancelado', 'Cancelado')],
        string='Estados', default='pendiente', readonly=True, copy=False,
        tracking=True)
    estado_id = fields.Integer('estado_id', default=1)
    adjuntos = fields.Integer(string='adjunto', store=True)
    negociar_terminos = fields.Boolean(string='Negociar Terminos',
                                       required=False)
    tipo_reunion = fields.Selection(string='Tipo Reunión',
                                    selection=[('presencial', 'Presencial'),
                                               ('distancia', 'A Distancia'), ],
                                    default='presencial', required=True, )
    modo_distancia = fields.Selection(string='Modo Distancia', selection=[
        ('correo', 'Correo electrónico'), ('audio', 'AudioConferencia'),
        ('video', 'VideoConferencia'), ], required=False, )
    resultado = fields.Html(string='Resultado', required=False)
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    cancelado = fields.Text(string='Motivo de cancelación', required=False)
    es_responsable = fields.Boolean(string='Es_responsable',
                                    compute='_compute_es_responsable')
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    # fechas formateadas
    fecha_inicio_formated = fields.Char(compute='_fecha_inicio_formated')
    fecha_fin_formated = fields.Char(compute='_fecha_fin_formated')

    def _fecha_inicio_formated(self):
        for part in self:
            part.fecha_inicio_formated = part.fecha_inicio.strftime("%d/%m/%Y")

    def _fecha_fin_formated(self):
        for part in self:
            part.fecha_fin_formated = part.fecha_fin.strftime("%d/%m/%Y")

    # validar si el usuario es el responsable
    def _compute_es_responsable(self):
        if self.responsable_id == self.env.user:
            self.es_responsable = True
        else:
            self.es_responsable = False

    # pasar a Pendiente
    def estado_pendiente(self):
        self.write({'estado': 'pendiente', 'estado_id': 1})
        # envió la notificación a los seguidores
        self.message_post(body='EL Acuerdo fue rechazado',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_reuniones.reunion_nuevo_acuerdo_rechazado')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)

    # pasar a En proceso
    def estado_en_proceso(self):
        if self.participantes_ids:
            self.write({'estado': 'proceso', 'estado_id': 2})

            # creo la lista de seguidores
            seguidor = self.participantes_ids
            # agrego los seguidores al modelo
            self.message_subscribe(partner_ids=seguidor.partner_id.ids)
            # envió la notificación a los seguidores
            self.message_post(body='Nuevo acuerdo asignado',
                              message_type='notification',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # mantiene actualizado el correo de los seguidores del registro
            correos = ''
            for follower in self.message_partner_ids:
                correos = str(correos) + str(follower.email_formatted)
            self.correo_seguidores = correos
            # envío el correo a los seguidores del registro
            local_context = self.env.context.copy()
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_nuevo_acuerdo_proceso')
            template.with_context(local_context).send_mail(self.id,
                                                           force_send=True)

        else:
            raise UserError(
                "Para continuar debe agregar a los ejecutantes del acuerdo.")

    # enviar a revision
    def estado_en_revision(self):
        self.write({'estado': 'revision', 'estado_id': 3})
        # creo la lista de seguidores
        seguidor = self.participantes_ids
        # agrego los seguidores al modelo
        self.message_subscribe(partner_ids=seguidor.partner_id.ids)
        # envió la notificación a los seguidores
        self.message_post(body='Acuerdo enviado a revisión',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_reuniones.reunion_nuevo_acuerdo_revision')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)

    # liberar para revision
    def estado_liberar(self):
        self.write({'estado': 'liberar', 'estado_id': 4})

        # busco usuarios con rol de secretaria
        secretaria = self.env.ref(
            'sicpro_app_reuniones.group_reuniones_secretaria').users
        # busco usuarios con rol de director
        director = self.env.ref(
            'sicpro_app_reuniones.group_reuniones_director').users
        # agrego los seguidores al modelo
        self.message_subscribe(partner_ids=director.partner_id.ids)

        # creo la lista de seguidores
        seguidor = secretaria + director
        # envió la notificación a los seguidores
        self.message_post(body='Un Acuerdo fue liberado',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in seguidor:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_reuniones.reunion_nuevo_acuerdo_liberar')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)

    # pasar a cumplido
    def estado_cumplido(self):
        self.write({'estado': 'cumplido', 'estado_id': 5})

        # envió la notificación a los seguidores
        self.message_post(body='EL Acuerdo está cumplido',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_reuniones.reunion_nuevo_acuerdo_cumplido')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)
        # animación de acuerdo cumplido
        rainbow = {'effect': {'fadeout': 'slow',
                              'message': 'Felicidades. El Acuerdo fue cumplido',
                              'type': 'rainbow_man', }}
        return rainbow

    # cancelar acuerdo
    def estado_cancelado(self):
        self.write({'estado': 'cancelado', 'estado_id': 6})
        # envió la notificación a los seguidores
        self.message_post(body='EL Acuerdo fue cancelado',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref(
            'sicpro_app_reuniones.reunion_nuevo_acuerdo_cancelado')
        template.with_context(local_context).send_mail(self.id,
                                                       force_send=True)

    # chequea que la fecha fin no sea anterior a la inicial
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_closing_date(self):
        for event in self:
            if event.fecha_fin < event.fecha_inicio:
                raise ValidationError(
                    _('La fecha fin no puede ser anterior a la fecha final.'))

    @api.model
    def acuerdos_vencimiento(self):
        fecha_control = fields.Date.context_today(self)
        data_fechas = self.env['sicpro.app.reuniones.acuerdos'].search(
            [('estado', 'in', ('pendiente', 'proceso', 'revision', 'liberar')),
             ])

        # actualizo los días pre finales
        for item in data_fechas:
            resta = fields.Date.from_string(
                item.fecha_fin) - fields.Date.from_string(fecha_control)
            item.fecha_pre_fin = resta.days

        data = self.env['sicpro.app.reuniones.acuerdos'].search(
            [('estado', 'in', ('pendiente', 'proceso', 'revision', 'liberar')),
             ('fecha_pre_fin', '<=', 3)])
        # raise ValidationError(data)

        if data:
            for item in data:
                if item.fecha_pre_fin <= 3 and item.fecha_pre_fin > 0:
                    # envió la notificación a los seguidores
                    item.message_post(body='El acuerdo está próximo a vencer',
                                      message_type='notification',
                                      subtype_xmlid='mail.mt_comment',
                                      author_id=self.env.user.partner_id.id)
                    # mantiene actualizado el correo de seguidores del registro
                    correos = ''
                    for follower in item.message_partner_ids:
                        correos = str(correos) + str(follower.email_formatted)
                    item.correo_seguidores = correos
                    # envío el correo a los seguidores del registro
                    local_context = data.env.context.copy()
                    template = data.env.ref(
                        'sicpro_app_reuniones.reunion_nuevo_acuerdo_proximo_vencer')
                    template.with_context(local_context).send_mail(item.id,
                                                                   force_send=True)
                elif item.fecha_pre_fin == 0:
                    # envió la notificación a los seguidores
                    item.message_post(body='El acuerdo está próximo a vencer',
                                      message_type='notification',
                                      subtype_xmlid='mail.mt_comment',
                                      author_id=self.env.user.partner_id.id)
                    # mantiene actualizado el correo de seguidores del registro
                    correos = ''
                    for follower in item.message_partner_ids:
                        correos = str(correos) + str(follower.email_formatted)
                    item.correo_seguidores = correos
                    # envío el correo a los seguidores del registro
                    local_context = data.env.context.copy()
                    template = data.env.ref(
                        'sicpro_app_reuniones.reunion_nuevo_acuerdo_vencido')
                    template.with_context(local_context).send_mail(item.id,
                                                                   force_send=True)


    @api.model_create_multi
    def create(self, vals_list):
        acuerdos = super(ReunionesAcuerdos, self).create(vals_list)
        for item in acuerdos:
            # creo la lista de seguidores
            seguidor = item['responsable_id']
            # agrego los seguidores al modelo
            item.message_subscribe(partner_ids=seguidor.partner_id.ids)
            # envió la notificación a los seguidores
            item.message_post(body='Ha sido asignado un nuevo acuerdo',
                              message_type='notification',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)

            # envío el correo electrónico
            correos = str(seguidor.email_formatted)
            item['correo_seguidores'] = correos
            # envío el correo a los seguidores del registro
            template = self.env.ref(
                'sicpro_app_reuniones.reunion_nuevo_acuerdo')
            template.send_mail(item.id, force_send=True)

        return acuerdos
