# -*- coding: utf-8 -*-


from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import os
import logging
from odoo.addons.smile_log.tools import SmileDBLogger
from datetime import datetime
import pytz


_logger = logging.getLogger(__name__)


class TrabajadoresAccionesDisiplinarias(models.Model):
    _name = 'sicpro.app.trabajadores.disiplinaria.acciones'
    _description = 'Medidas disciplinarias'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_solicitante(self):
        solicitante = self.env.user.trabajador.id
        return solicitante


    estado = fields.Selection(
        [('borrador', 'Borrador'), ('espera_accion', 'Esperando acción'),
            ('action', 'Acción validada'), ('cancelado', 'Cancelado'), ],
        default='borrador', tracking=True)

    name = fields.Char(string='Referencia', required=False, copy=False,
                       readonly=False,)
    user_id = fields.Many2one('res.users', index=True, tracking=True,
                              default=lambda self: self.env.uid)
    solicita_medida = fields.Many2one('sicpro.app.trabajadores',
                                      string='Solicitante', required=True,
                                      default=_default_solicitante)
    cargo_solicitante = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                                        string='Cargo', store=True,
                                        related='solicita_medida.ocupacion_id')
    departamento_solicitante = fields.Many2one('sicpro.app.trabajadores.areas',
                                        string='Departamento', store=True,
                                        related='solicita_medida.area_id')
    company_id = fields.Many2one('res.company', store=True, readonly=False,
                                 related='trabajador_id.company_id')
    trabajador_id = fields.Many2one('sicpro.app.trabajadores',
                                    string='Trabajador', required=True,)
    departamento = fields.Many2one(
        'sicpro.app.trabajadores.areas', string='Área',
        related='trabajador_id.area_id', store=True)
    fecha_incorporacion = fields.Date(string="Incorporación",
        related='trabajador_id.fecha_incorporacion', store=True)
    equipo_tecnico = fields.Many2one("sicpro.app.trabajadores.equipo.tecnico",
        string="Equipo Técnico", related='trabajador_id.equipo_tecnico')
    motivo = fields.Many2one('sicpro.app.trabajadores.disiplinaria.categorias',
        string='Motivo', required=True)
    action = fields.Many2one('sicpro.app.trabajadores.disiplinaria.categorias',
                             string="Medida")
    dias_validacion = fields.Integer(string='Días', required=False,
                                     related='action.vigencia',
                                     store=True)
    acciones_detalles = fields.Text(string="Detalles de la acción")
    attachment_ids = fields.Many2many('ir.attachment', string="Adjuntos")
    note = fields.Text(string="Notas")
    fecha_infraccion = fields.Datetime(string="Fecha de Infracción", required=True)
    fecha_solicitud = fields.Date(string="Medida solicitada",
                                  default=lambda self: fields.Date.context_today(self))
    fecha_emision = fields.Date(string="Medida emitida",
                                compute='_compute_action')
    fecha_notificacion = fields.Date(string="Trabajador notificado",
                                     compute='_compute_action')
    fecha_expiracion = fields.Datetime(string='Fecha de Expiración', readonly=False)
    active = fields.Boolean('Activo', default=True)
    correo_seguidores = fields.Char(string="correo_seguidores", index=True)
    estado_secundario = fields.Char(string='estado_secundario',
                                    default='Borrador')
    motivo_description = fields.Text(string="Detalles del motivo",
                                     related='motivo.description')
    accion_description = fields.Text(string="Detalles la acción",
                                     related='action.description')
    solicitante_fecha_conocimiento = fields.Date(
        string="Fecha Conocimiento",)
    solicitante_via_conocimiento = fields.Char(string='Vía de Conocimiento')
    cargo = fields.Many2one('sicpro.app.trabajadores.ocupacion',
                            string='Cargo:', store=True,
                            related='trabajador_id.ocupacion_id')
    fecha_contrato = fields.Date(string="Contratación", store=True,
                                 related='trabajador_id.inicio_contrato')
    categoria_ocupacional = fields.Many2one(
        'sicpro.app.trabajadores.categorias', string='Categoría',
        store=True, related='trabajador_id.categoria_ocupacional')
    fecha_infraccion_formated = fields.Char(
        compute='_fecha_infraccion_formated')
    fecha_expiracion_formated = fields.Char(
        compute='_fecha_expiracion_formated')

    def _fecha_infraccion_formated(self):
        user_tz = self.env.user.tz or pytz.utc
        local = pytz.timezone(user_tz)
        for part in self:
            part.fecha_infraccion_formated = datetime.strftime(
                pytz.utc.localize(part.fecha_infraccion).astimezone(local),
                "%d/%m/%Y, %H:%M:%S")

    def _fecha_expiracion_formated(self):
        if self.fecha_expiracion:
            user_tz = self.env.user.tz or pytz.utc
            local = pytz.timezone(user_tz)
            for part in self:
                part.fecha_expiracion_formated = datetime.strftime(
                    pytz.utc.localize(part.fecha_expiracion).astimezone(local),
                    "%d/%m/%Y, %H:%M:%S")
        else:
            self.fecha_expiracion_formated = None

    @api.depends('fecha_notificacion','action')
    @api.onchange('fecha_notificacion', 'action')
    def _onchange_fecha_notificacion(self):
        if self.fecha_notificacion:
            date_1 = fields.Date.from_string(self.fecha_notificacion)
            date_2 = date_1 + relativedelta(days=self.dias_validacion)
            self.fecha_expiracion = date_2
        else:
            self.fecha_expiracion = None

    @api.onchange('trabajador_id')
    @api.depends('trabajador_id')
    def onchange_trabajador_id(self):
        if self.estado == 'action':
            raise ValidationError(_('No puede editar una acción validada !!'))

    @api.onchange('motivo')
    @api.depends('motivo')
    def onchange_reason(self):
        if self.estado == 'action':
            raise ValidationError(_('No puede editar una acción validada !!'))

    @api.depends('action')
    def _compute_action(self):
        if self.action:
            self.fecha_emision = fields.datetime.today()
            self.fecha_notificacion = fields.Date.context_today(self) + timedelta(days=1)
        else:
            self.fecha_emision = None
            self.fecha_notificacion = None

    def assign_function(self):
        # envió la notificación a los seguidores
        self.message_post(body='Solicitud de Medida en espera de revisión',
            message_type='notification', subtype_xmlid='mail.mt_comment',
            author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.motivo, self.env.user.name]
        logger.time_info('[%s] Cambio de estado: La solicitud de medida paso '
                         'al estado de Espera por revisión - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(data_log))
        for rec in self:
            rec.estado = 'espera_accion'
            rec.estado_secundario = 'Esperando Acción'
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
        template.with_context(local_context).send_mail(self.id, force_send=True)

    def cancel_function(self):
        # envió la notificación a los seguidores
        self.message_post(body='Solicitud de Medida cancelada',
            message_type='notification', subtype_xmlid='mail.mt_comment',
            author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.motivo, self.env.user.name]
        logger.time_info('[%s] Cambio de estado: La solicitud de medida fue '
                         'cancelada - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))
        for rec in self:
            rec.estado = 'cancelado'
            rec.estado_secundario = 'Cancelado'
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
        template.with_context(local_context).send_mail(self.id, force_send=True)

    def set_to_function(self):
        # envió la notificación a los seguidores
        self.message_post(body='Solicitud de Medida en estado de borrador',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # Registro del log
        logger = SmileDBLogger(self._cr.dbname, self._name, self.id, self._uid)
        pid = os.getpid()
        data_log = [pid, self._name, self.id, self.motivo, self.env.user.name]
        logger.time_info('[%s] Cambio de estado: La solicitud de medida paso '
                         'al estado de Borrador - '
                         'Records: %s (%s) - %s. Usuario: %s - ' % tuple(
            data_log))
        for rec in self:
            rec.estado = 'borrador'
            rec.estado_secundario = 'Borrador'
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
        template.with_context(local_context).send_mail(self.id, force_send=True)

    def action_function(self):
        for rec in self:
            if not rec.action:
                raise ValidationError(
                    _('Tienes que seleccionar una acción !!'))
            if not rec.acciones_detalles:
                raise ValidationError(
                    _('Tienes que completar la información de la acción !!'))
            # envió la notificación a los seguidores
            self.message_post(body='Solicitud de Medida validada',
                              message_type='notification',
                              subtype_xmlid='mail.mt_comment',
                              author_id=self.env.user.partner_id.id)
            # Registro del log
            logger = SmileDBLogger(self._cr.dbname, self._name, self.id,
                                   self._uid)
            pid = os.getpid()
            data_log = [pid, self._name, self.id, self.motivo,
                        self.env.user.name]
            logger.time_info(
                '[%s] Cambio de estado: La solicitud de medida paso '
                'al estado de Validado - '
                'Records: %s (%s) - %s. Usuario: %s - ' % tuple(data_log))
            rec.estado = 'action'
            rec.estado_secundario = 'Medida Validada'
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in self.message_partner_ids:
            correos = str(correos) + str(follower.email_formatted)
        self.correo_seguidores = correos
        # envío el correo a los seguidores del registro
        local_context = self.env.context.copy()
        template = self.env.ref('sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_cambios')
        template.with_context(local_context).send_mail(self.id, force_send=True)

    # desactivo la medida del trabajador y envío notificación y correo
    def send_expira_medida_mail(self):
        date = str(datetime.now().date().strftime('%d/%m/%Y'))
        trabajador = self.env[
            'sicpro.app.trabajadores.disiplinaria.acciones'].search(
            ['&', ('active', '=', True), ('fecha_expiracion', '=', date)])
        if trabajador:
            for emp in trabajador:
                # envió la notificación a los seguidores
                emp.message_post(body='Expiró una Medida disciplinaria',
                                 message_type='notification',
                                 subtype_xmlid='mail.mt_comment',
                                 author_id=self.env.user.partner_id.id)
                # desactivo el registro
                emp.active = False
                # mantiene actualizado el correo de los seguidores del registro
                correos = ''
                for follower in emp.message_partner_ids:
                    correos = str(correos) + str(follower.email_formatted)
                emp.correo_seguidores = correos
                template = self.env.ref(
                    'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_expira')
                template.send_mail(emp.id, force_send=True)

    @api.model
    def create(self, vals):
        disciplinario = super(TrabajadoresAccionesDisiplinarias, self).create(vals)
        # asignar la secuencia para el registro
        disciplinario['name'] = self.env['ir.sequence'].next_by_code('medidas_disciplinarias')
        # suscribir automáticamente al modelo
        # busco el id del trabajador que se le aplica la medida
        trabajador = self.env['sicpro.app.trabajadores'].search(
            [('id', '=', vals.get('trabajador_id')),])
        # busco el lider del grupo de atención al trabajador
        lider = trabajador.equipo_tecnico.lider.user_id
        # busco los técnicos que atienden al trabajador
        tecnicos = trabajador.equipo_tecnico.member_ids.user_id
        # busco los responsables de la aplicación de trabajadores
        responsables = self.env.ref(
            'sicpro_app_trabajadores.grupo_app_trabajador_responsable').users
        # busco el encargado legal del proceso
        legal = self.env.ref(
            'sicpro_app_trabajadores.grupo_app_trabajador_disciplina_legal').users
        # busco los representantes del proceso del trabajador afectado
        representantes_proceso = self.env.ref(
            'sicpro_app_trabajadores.grupo_app_trabajador_disciplina_jefe').users.ids
        representantes = self.env['res.users'].search(
            ['&', ('company_id', '=', trabajador.company_id.id),
             ('id', 'in', representantes_proceso)])
        # creo la lista de seguidores
        seguidores = tecnicos + lider + responsables + legal + representantes
        # agrego los seguidores al modelo
        disciplinario.message_subscribe(partner_ids=seguidores.partner_id.ids)
        # envió la notificación a los seguidores
        disciplinario.message_post(body='Nueva medida disciplinaria en borrador',
                          message_type='notification',
                          subtype_xmlid='mail.mt_comment',
                          author_id=self.env.user.partner_id.id)
        # mantiene actualizado el correo de los seguidores del registro
        correos = ''
        for follower in seguidores:
            correos = str(correos) + str(follower.email_formatted)
        disciplinario['correo_seguidores'] = correos
        # envío el correo a los seguidores del registro
        template = self.env.ref(
            'sicpro_app_trabajadores.trabajadores_medidas_disciplinarias_nueva')
        template.send_mail(disciplinario.id, force_send=True)

        return disciplinario

